# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:44:28 2022

@author: DanielT17
"""

# %% Imports

import numpy as np
from Utils import Bytearray_To_Int,Turn_Bitstring_To_Numpy_Array_Of_Bits,Int_To_Bytearray,Turn_Numpy_Array_Of_Bits_To_Bitstring,Unique
from Polynomial_Reversing_Method_2 import Poly_Mod,Packet_Concatenate
from Polynomial_Utils import Create_Valid_Unequal_Packet_Combinations,Generate_All_Poly_Representations
from itertools import product


# %% Functions

def Get_Packet_Estimate_Message_Length_Binary(packet):
    '''
    Description:
        This function gets a packet and estimates the message length.
    Inputs:
        packet - list - a list where the first entry is the message and the 
        second is the crc.
    Outputs:
        message_len - int - calculates the length of the message part of the 
        packet.
    '''
    message = packet[0]
    message_len = len(bin(Bytearray_To_Int(message))[2:])
    return message_len

def Build_Relative_Shift_Matrix(l1,l2,poly,crc_width):
    '''
    Description:
        This function creates the following matrix x^k * (x^l1 + x^l2) mod p.
        This matrix is the relative shift matrix which is described in GF(2)
    Inputs:
        l1 - int - length of message one in bits.
        l2 - int - length of message two in bits.
        poly - int - estimated crc polynomial in intger representation.
        crc_width - int - the crc polynomial width
    Outputs:
        matrix - numpy array - A matrix description of the equation above in GF(2).
    '''
    matrix = np.zeros((crc_width,crc_width),dtype=np.uint8)
    for k in range(crc_width):
        matrix_row = bin(Poly_Mod((2**(k)) * (2**(l1) + 2**(l2)),poly))[2:]
        matrix_row = '0' * (crc_width-len(matrix_row)) + matrix_row
        matrix[k,:] = Turn_Bitstring_To_Numpy_Array_Of_Bits(matrix_row,crc_width)
    matrix = np.transpose(matrix)
    return matrix

def Run_Relative_Shift_Matrix(packet1,packet2,poly,crc_width):
    '''
    Description:
        This function does the relevant preprocessing to calculate the relative
        shift matrix, after being done with the preprocessing it calculates, 
        the relative shift matrix, and returns it.
    Inputs:
        packet1,packet2 - lists - lists where the first entry is the message 
        and the second is the crc.
        poly - int - estimated crc polynomial in intger representation.
        crc_width - int - the crc polynomial width
    Outputs:
        matrix - numpy array - A matrix description of the equation above in GF(2).
    '''
    packet1_len = Get_Packet_Estimate_Message_Length_Binary(packet1) 
    packet2_len = Get_Packet_Estimate_Message_Length_Binary(packet2)
    matrix = Build_Relative_Shift_Matrix(packet1_len,packet2_len,poly,crc_width)
    return matrix

def Create_Target_Vector(packet1,packet2,poly,crc_width,crc_family):
    '''
    Description:
        This function creates the target vector which will be used to solve
        the value of xor_in.
    Inputs:
        packet1,packet2 - lists - lists where the first entry is the message 
        and the second is the crc.
        poly - int - estimated crc polynomial in intger representation.
        crc_width - int - the crc polynomial width.
        crc_family - int - what type of preprocessing should be done.
    Outputs:
        target_vector - numpy array - the target vector in GF(2).
    '''
    if crc_family == 0:
        endian1 = 'little'; endian2 = 'little'
        packet1_int =  Bytearray_To_Int(packet1[0] + Int_To_Bytearray(Bytearray_To_Int(packet1[1]),endian1),endian2)
        packet2_int =  Bytearray_To_Int(packet2[0] + Int_To_Bytearray(Bytearray_To_Int(packet2[1]),endian1),endian2)
    elif crc_family == 1:
        packet1_int = Packet_Concatenate(packet1)
        packet2_int = Packet_Concatenate(packet2)
    packet_diff = packet1_int ^ packet2_int
    target_vector = Poly_Mod(packet_diff,poly)
    target_vector = bin(target_vector)[2:]
    if len(target_vector) != crc_width:
        target_vector = '0' * (crc_width-len(target_vector)) + target_vector
    target_vector = np.transpose(Turn_Bitstring_To_Numpy_Array_Of_Bits(target_vector,crc_width))
    return target_vector
    
def Gauss_Jordan_Elimination_In_GF_2(matrix_original,vector_original):
    '''
    Description:
        Gauss Jordan elimination in GF(2) the function gets amtrix which represent
        the coefficents, and a target vector, and finds the solution to the linear
        equation.
    Inputs:
        matrix_original - numpy array - matrix of coefficents.
        vector_original - numpy array - target vector.
    Outputs:
        matrix - numpy array - matrix in row echlon form.
        vector - numpy array - solution to the linear equation.
    '''
    matrix = np.concatenate((matrix_original,vector_original),1)
    m,n = matrix.shape; i=0; j=0;
    while i < m and j < n:
        k = np.argmax(matrix[i:, j]) +i
        matrix[[k, i]] = matrix[[i, k]]
        aijn = matrix[i, j:]
        col = np.copy(matrix[:, j])
        col[i] = 0
        flip = np.outer(col, aijn)
        matrix[:, j:] = matrix[:, j:] ^ flip
        i += 1; j +=1
    return matrix[:,:-1],matrix[:,-1]    

def Check_If_Soultion_Exists(mat,xor_in):
    '''
    Description:
        This function takes gets a matrix in row echlon form and checks if a solution
        exists for the matrix.
    Inputs:
        mat - numpy array - matrix in row echlon form.
        and the second is the crc.
        vec - numpy array - vector in GF(2).
    Outputs:
        zero_rows - numpy array - rows which result in infinte number of solutions.
    '''
    zero_rows = np.where(~mat.any(axis=1))[0]
    for zero_row in zero_rows:
        if np.any(xor_in[zero_rows] != [0]*len(xor_in[zero_rows])):
            raise Exception('Equation is unsolvable!')
    return zero_rows

def Create_All_Possible_Vec_Combinations(mat,vec,zero_rows):
    '''
    Description:
        This function creates a list of vectors to check the soultion aginst,
        in case there is more than one solution.
    Inputs:
        mat - numpy array - matrix in row echlon form.
        and the second is the crc.
        vec - numpy array - vector in GF(2).
        zero_rows - numpy array - array of the rows which contain full zeros.
    Outputs:
        mat_new - numpy array - matrix to test the solutions against.
        vecs - list of vectors - list of vectors to check the solution against
    '''
    mat_new = mat.copy()
    for zero_row in zero_rows:
        mat_new[zero_row,zero_row] = 1
    vecs = []
    combination =["".join(seq) for seq in product("01", repeat=len(zero_rows))]
    for seq in combination:
        vec_new = vec.copy()
        for ind,row in enumerate(zero_rows):
            vec_new[row] = int(seq[ind])
        vecs.append(vec_new)
    return mat_new,vecs

def Estimate_Xor_In(packet1,packet2,poly,crc_width,crc_family):
    '''
    Description:
        This function takes two packets of unequal length and a polynomial, and
        Estimates the corresponding Xor In value.
    Inputs:
        packet1,packet2 - lists - lists where the first entry is the message 
        and the second is the crc.
        poly - int - estimated crc polynomial in intger representation.
        crc_width - int - the crc polynomial width.
        crc_family - int - what type of preprocessing should be done.
    Outputs:
        xor_in - binary string - estimated xor_in binary string.
    '''
    vector = Create_Target_Vector(packet1,packet2,poly,crc_width,crc_family)
    matrix = Run_Relative_Shift_Matrix(packet1,packet2,poly,crc_width)
    mat, vec_solution = Gauss_Jordan_Elimination_In_GF_2(matrix,vector)
    if np.sum(mat) == 0 and np.sum(vec_solution) == 0:
        xor_in = np.array([1]*crc_width,dtype = np.uint8)
        xor_in = int(Turn_Numpy_Array_Of_Bits_To_Bitstring(xor_in,crc_width),2)
        xor_in = [xor_in]
    else:
        xor_in = []
        try:
            zero_rows = Check_If_Soultion_Exists(mat,vec_solution)
            if len(zero_rows) > 0 and len(zero_rows)<5:
                mat_new, vecs = Create_All_Possible_Vec_Combinations(mat,vec_solution,zero_rows)
                for cur_vector in vecs:
                   _,cur_xor_in = Gauss_Jordan_Elimination_In_GF_2(mat_new,np.reshape(cur_vector,(crc_width,1)))
                   xor_in.append(int(Turn_Numpy_Array_Of_Bits_To_Bitstring(cur_xor_in,crc_width),2))
        except: pass
    return xor_in   

def Estimate_Xor_In_All_Possiblities(second_step_packets,polys,crc_width):
    '''
    Description:
        This function gets a list of packets and a list of polynomials and brute
        forces over all possible combinations the correct xor in value with its
        generator polynomial (taps), and actul polynomial.
    Inputs:
        second_step_packets - list - a list of pacekts.
        polys - list - a list of estimated polynomials by method 1.
        crc_width - int - the crc polynomial width
    Outputs:
        generator_polys - list - a list of valid generator polynomials.
        useful_polys - list - a list of actual polynomials which result in valid,
        xor_in value.
        useful_xor_in - list - a list of possible xor_in values.
    '''
    packet_combinations = Create_Valid_Unequal_Packet_Combinations(second_step_packets)
    crc_families = [0,1]
    generator_polys = []; useful_polys = []; useful_xor_in = [];
    for cur_poly in polys:
        possible_polys = Generate_All_Poly_Representations(cur_poly,crc_width,enb_combinations=True)
        for possible_poly in possible_polys:
            xor_in_ls = []
            for crc_family in crc_families:
                for combination in packet_combinations:
                    xor_in_ls = xor_in_ls + Estimate_Xor_In(combination[0],combination[1],possible_poly,crc_width,crc_family)
                xor_in_ls.append(int((crc_width//4)*'f',16)); xor_in_ls.append(0) # append special cases
                xor_in_unique,counts = Unique(xor_in_ls)
                if len(np.where(2<=np.array(counts))[0]) != 0:
                    generator_polys.append(cur_poly)
                    useful_polys.append(possible_poly)
                    useful_xor_in.append(list(xor_in_unique))
    return generator_polys,useful_polys,useful_xor_in

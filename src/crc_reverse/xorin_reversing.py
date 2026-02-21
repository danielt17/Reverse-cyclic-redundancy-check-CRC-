# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:44:28 2022

@author: DanielT17
"""

# %% Imports

import numpy as np
from .utils import bytearray_to_int,turn_bitstring_to_numpy_array_of_bits,int_to_bytearray,turn_numpy_array_of_bits_to_bitstring,unique
from .polynomial_reversing_method_2 import poly_mod,packet_concatenate
from .polynomial_utils import create_valid_unequal_packet_combinations,generate_all_poly_representations
from itertools import product
from numpy.typing import NDArray
from typing import Sequence, cast


# %% Functions

PacketPair = list[bytes]


def get_packet_estimate_message_length_binary(packet: PacketPair) -> int:
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
    message_len = len(bin(bytearray_to_int(message))[2:])
    return message_len

def build_relative_shift_matrix(l1: int, l2: int, poly: int, crc_width: int) -> NDArray[np.uint8]:
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
        matrix_row = bin(poly_mod((2**(k)) * (2**(l1) + 2**(l2)),poly))[2:]
        matrix_row = '0' * (crc_width-len(matrix_row)) + matrix_row
        matrix[k,:] = turn_bitstring_to_numpy_array_of_bits(matrix_row,crc_width)
    matrix = np.transpose(matrix)
    return matrix

def run_relative_shift_matrix(packet1: PacketPair, packet2: PacketPair, poly: int, crc_width: int) -> NDArray[np.uint8]:
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
    packet1_len = get_packet_estimate_message_length_binary(packet1) 
    packet2_len = get_packet_estimate_message_length_binary(packet2)
    matrix = build_relative_shift_matrix(packet1_len,packet2_len,poly,crc_width)
    return matrix

def create_target_vector(
    packet1: PacketPair, packet2: PacketPair, poly: int, crc_width: int, crc_family: int
) -> NDArray[np.uint8]:
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
        packet1_int =  bytearray_to_int(packet1[0] + int_to_bytearray(bytearray_to_int(packet1[1]),endian1),endian2)
        packet2_int =  bytearray_to_int(packet2[0] + int_to_bytearray(bytearray_to_int(packet2[1]),endian1),endian2)
    elif crc_family == 1:
        packet1_int = packet_concatenate(packet1)
        packet2_int = packet_concatenate(packet2)
    else:
        raise ValueError("crc_family must be 0 or 1")
    packet_diff = packet1_int ^ packet2_int
    target_vector = poly_mod(packet_diff,poly)
    target_vector = bin(target_vector)[2:]
    if len(target_vector) != crc_width:
        target_vector = '0' * (crc_width-len(target_vector)) + target_vector
    target_vector = np.transpose(turn_bitstring_to_numpy_array_of_bits(target_vector,crc_width))
    return target_vector
    
def gauss_jordan_elimination_in_gf_2(
    matrix_original: NDArray[np.uint8], vector_original: NDArray[np.uint8]
) -> tuple[NDArray[np.uint8], NDArray[np.uint8]]:
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

def check_if_soultion_exists(mat: NDArray[np.uint8], xor_in: NDArray[np.uint8]) -> NDArray[np.intp]:
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
    for _ in zero_rows:
        if np.any(xor_in[zero_rows] != [0] * len(xor_in[zero_rows])):
            raise Exception('Equation is unsolvable!')
    return zero_rows

def create_all_possible_vec_combinations(
    mat: NDArray[np.uint8], vec: NDArray[np.uint8], zero_rows: NDArray[np.intp]
) -> tuple[NDArray[np.uint8], list[NDArray[np.uint8]]]:
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
    vecs: list[NDArray[np.uint8]] = []
    combination =["".join(seq) for seq in product("01", repeat=len(zero_rows))]
    for seq in combination:
        vec_new = vec.copy()
        for ind,row in enumerate(zero_rows):
            vec_new[row] = int(seq[ind])
        vecs.append(vec_new)
    return mat_new,vecs

def estimate_xor_in(packet1: PacketPair, packet2: PacketPair, poly: int, crc_width: int, crc_family: int) -> list[int]:
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
    vector = create_target_vector(packet1,packet2,poly,crc_width,crc_family)
    matrix = run_relative_shift_matrix(packet1,packet2,poly,crc_width)
    mat, vec_solution = gauss_jordan_elimination_in_gf_2(matrix,vector)
    if np.sum(mat) == 0 and np.sum(vec_solution) == 0:
        xor_in = np.array([1]*crc_width,dtype = np.uint8)
        xor_in = int(turn_numpy_array_of_bits_to_bitstring(xor_in,crc_width),2)
        xor_in = [xor_in]
    else:
        xor_in = []
        try:
            zero_rows = check_if_soultion_exists(mat,vec_solution)
            if len(zero_rows) > 0 and len(zero_rows)<5:
                mat_new, vecs = create_all_possible_vec_combinations(mat,vec_solution,zero_rows)
                for cur_vector in vecs:
                   _,cur_xor_in = gauss_jordan_elimination_in_gf_2(mat_new,np.reshape(cur_vector,(crc_width,1)))
                   xor_in.append(int(turn_numpy_array_of_bits_to_bitstring(cur_xor_in,crc_width),2))
        except: pass
    return xor_in   

def estimate_xor_in_all_possiblities(
    second_step_packets: list[PacketPair], polys: Sequence[int], crc_width: int
) -> tuple[list[int], list[int], list[list[int]]]:
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
    packet_combinations = create_valid_unequal_packet_combinations(second_step_packets)
    crc_families = [0,1]
    generator_polys = []; useful_polys = []; useful_xor_in = [];
    for cur_poly in polys:
        possible_polys = generate_all_poly_representations(cur_poly,crc_width,enb_combinations=True)
        for possible_poly in possible_polys:
            xor_in_ls = []
            for crc_family in crc_families:
                for combination in packet_combinations:
                    xor_in_ls = xor_in_ls + estimate_xor_in(combination[0],combination[1],possible_poly,crc_width,crc_family)
                xor_in_ls.append(int((crc_width//4)*'f',16)); xor_in_ls.append(0) # append special cases
                xor_in_unique, counts = unique(xor_in_ls)
                xor_in_unique = cast(list[int], xor_in_unique)
                if len(np.where(2<=np.array(counts))[0]) != 0:
                    generator_polys.append(cur_poly)
                    useful_polys.append(possible_poly)
                    useful_xor_in.append(xor_in_unique)
    return generator_polys,useful_polys,useful_xor_in

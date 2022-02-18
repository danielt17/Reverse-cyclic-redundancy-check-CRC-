# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 17:51:57 2022

@author: danie
"""


# %% Imports

import crcengine 
import numpy as np
from time import sleep
from Crypto.Util.number import long_to_bytes
import FiniteFieldAlgebra as Field
import itertools

# %% Functions

# Based on: https://www.cosc.canterbury.ac.nz/greg.ewing/essays/CRC-Reverse-Engineering.html

def reverse_poly(string_poly,order):
    # reversing polynomial (shift is done to make sure the length is correct)
    len_string = order - len(bin(string_poly)[2:])
    return int(bin(string_poly)[::-1][:-2],2) << len_string

def recipolar_poly(string_poly,order):
    # recipolar_poly p(x) -> p(x^(-1))*x^n
    temp = bin(string_poly)[::-1][:-2][1:]
    temp = temp  + '0'*(order-len(temp)-1) + '1'
    return int(temp,2)

def reverse_recipolar_poly(string_poly,order):
    return reverse_poly(recipolar_poly(string_poly,order),order)

def byte_xor(ba1, ba2):
    # This function calculates the xor between two bytearrays
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def print_crc_parameters(crc_algorithm_name):
    # This function prints our crc algorithm of choice parameters
    params = crcengine.get_algorithm_params(crc_algorithm_name)
    print('Cyclic redundancy check parameters: \n')
    for _,param in enumerate(params.items()):
        if param[0] == 'poly':
            print('poly: ' + str(hex(param[1])))
        else:
            print(str(param[0]) + ': ' + str(param[1]) + '.')
    print('\n')
    sleep(5)
    return params

def calculate_and_print_result(input_string,crc_algorithm,enb_text=False):
    result = crc_algorithm(input_string)
    if enb_text == True:
        print('Input string: ' + str(input_string) + '\n')
        print('CRC int = ' + str(result) + '. Hex = 0x{:08x}'.format(result) + '\n')
    return result

def differential_message(str1,str2,crc_algorithm,print_text=True):
    # str1 and str2 are bytearray inputs
    # print('We compute a differential (homogenous) message, removing XorIn and XorOut from the equation')
    # C1 + C2 = (T^n(I) + D1 + F) + (T^n(I) + D2 + F) =	D1 + D2 (+ = XOR = addition in GF(2))
    if print_text:
        print('bytearray1 = ' + str(int.from_bytes(str1, "big")))
        print('bytearray2 = ' + str(int.from_bytes(str2, "big")))
        print('Effective differential (homogenous) CRC (bytearray1 XOR bytearray2) = ' + str(int.from_bytes(byte_xor(str1,str2), "big")) + '\n')
    crc1 = calculate_and_print_result(str1,crc_algorithm)
    crc2 = calculate_and_print_result(str2,crc_algorithm)
    diff_crc = crc1 ^ crc2
    return diff_crc

def estimate_poly_equation(diff_crc1,diff_crc2):
    # diff_crc2 is bigger than diff_crc1 with respect to the input to the input to the diff crc
    # We need a spanning basis to reverse the polynomial of the crc therefore
    # diff_crc are the differntial message (Homgenous) output of the differntial message algorithm
    # such that CRC(2^n) and CRC(2^(n+1)) are used to get the polynomial charateristic
    poly = (diff_crc2>>1)^diff_crc1
    return poly

def full_process_to_poly(str1,str2,str3,str4,crc_algorithm):
    # Putting everything togther
    diff_crc1 = differential_message(str1,str2,crc_algorithm)
    diff_crc2 = differential_message(str3,str4,crc_algorithm)
    poly = estimate_poly_equation(diff_crc1,diff_crc2)
    print('Estimated polynomial: ' + str(hex(poly)) + '\n')
    return poly

def guess_poly(crc_algorithm):
    print('Trying different input bytearray combinations in order to estimate the CRC polynomial using a differential method.\n')
    str1 = bytearray([0,0,0,0,0,0,0,10]);   str2 = bytearray([0,0,0,0,0,0,0,8]);  # 2
    str3 = bytearray([0,0,0,0,0,0,0,8]);    str4 = bytearray([0,0,0,0,0,0,0,12]); # 4
    str5 = bytearray([0,0,0,0,0,0,0,12]);   str6 = bytearray([0,0,0,0,0,0,0,4]);  # 8
    str7 = bytearray([0,0,0,0,0,0,0,24]);   str8 = bytearray([0,0,0,0,0,0,0,8]);  # 16
    strs = [str1, str2, str3, str4, str5, str6, str7, str8];
    amount_of_quads = len(strs)//2 - 1
    polys = []
    print('LSB path:\n')
    for i in range(amount_of_quads):
        poly = full_process_to_poly(strs[2*i],strs[2*i+1],strs[2*i+2],strs[2*i+3],crc_algorithm)
        polys.append(poly)
    for string in strs:
        string.reverse()
    print('MSB path:\n')
    for i in range(amount_of_quads):
        poly = full_process_to_poly(strs[2*i],strs[2*i+1],strs[2*i+2],strs[2*i+3],crc_algorithm)
        if poly == 0:
            continue
        polys.append(poly)
    polys = np.asarray(polys,np.uint64)
    polys = polys[polys != 0]
    values, counts = np.unique(polys, return_counts=True)
    ind = np.argmax(counts)
    estimated_poly_reverse = int(values[ind])
    estimated_poly_deg = len(bin(estimated_poly_reverse)[2:])
    estimated_poly_normal = reverse_poly(estimated_poly_reverse,estimated_poly_deg)
    estimated_poly_recipolar = recipolar_poly(estimated_poly_normal,estimated_poly_deg)
    estimated_poly_recipolar_reverese = reverse_recipolar_poly(estimated_poly_normal,estimated_poly_deg)
    print('\n')
    print('----------------------------------------\n')
    print('Estimated CRC polynomial:')
    print('Normal mode: ' + str(hex(estimated_poly_normal)))
    print('Reverse mode: ' + str(hex(estimated_poly_reverse)))
    print('Recipolar mode: ' + str(hex(estimated_poly_recipolar)))
    print('Reversed recipolar mode: ' + str(hex(estimated_poly_recipolar_reverese)))
    print('Polynomial degree: ' + str(estimated_poly_deg) + '\n')
    print('----------------------------------------\n')
    return estimated_poly_normal,estimated_poly_reverse,estimated_poly_recipolar,estimated_poly_recipolar_reverese,estimated_poly_deg

def preform_vector_gauss_jordan(K,REF_recipe_ls,RREF_recipe_ls):
    f = Field.PrimeField(2)
    K_mat = Field.Matrix(K.shape[0], K.shape[1], f)
    rows = K.shape[0]
    for i in range(K.shape[0]):
        K_mat.set(i, 0, int(K[i]))
    for ind in range(len(REF_recipe_ls)):
        numpivots = REF_recipe_ls[ind][1]
        pivotrow = REF_recipe_ls[ind][2]
        val_pivot_row = REF_recipe_ls[ind][3]
        multiple_values = REF_recipe_ls[ind][4]
        K_mat.swap_rows(numpivots, pivotrow)
        pivotrow = numpivots
        numpivots += 1
        K_mat.multiply_row(pivotrow, val_pivot_row)
        counter = 0
        for i in range(pivotrow + 1, rows):
            K_mat.add_rows(pivotrow, i, multiple_values[counter])
            counter = counter + 1
    for ind in range(len(RREF_recipe_ls)):
        i = RREF_recipe_ls[ind][0]
        neg_values = RREF_recipe_ls[ind][2]
        counter = 0
        for j in range(i):
            K_mat.add_rows(i, j, neg_values[counter])
            counter = counter + 1
    return K_mat

def solve_system_of_equations_over_gf2(T,K):
    # Solves system of equation A*x=b over GF(2)
    print('We want to find I such that: T*I=K over GF(2)\n')
    f = Field.PrimeField(2)
    T_mat = Field.Matrix(estimated_poly_deg, estimated_poly_deg, f)
    for i in range(estimated_poly_deg):
        for j in range(estimated_poly_deg):
            T_mat.set(i, j, int(T[i,j]))
    print('Initial T matrix: \n')
    for i in range(T_mat.row_count()): print(" ".join(str(T_mat.get(i, j)) for j in range(T_mat.column_count())))
    print('\n')
    print('Initial K vector: \n')
    print(K)
    print('\n')
    REF_recipe_ls,RREF_recipe_ls = T_mat.reduced_row_echelon_form()
    print('The reduced T matrix: \n')
    for i in range(T_mat.row_count()): print(" ".join(str(T_mat.get(i, j)) for j in range(T_mat.column_count())))
    K_mat = preform_vector_gauss_jordan(K,REF_recipe_ls,RREF_recipe_ls)
    print('\n')
    print('The reduced K vector: \n')
    for i in range(K_mat.row_count()): print(" ".join(str(K_mat.get(i, j)) for j in range(K_mat.column_count())))
    print('\n')
    T = np.array(T_mat.values)
    K = np.array(K_mat.values)
    zero_rows = np.where(~T.any(axis=1))[0]
    for zero_row in zero_rows:
        if K[zero_rows] != 0:
            raise Exception('Equation is unsolvable!')
    amount_of_zero_rows = len(zero_rows)
    for zero_row in zero_rows:
        T[zero_row,zero_row] = 1
    Ks = []
    combination =["".join(seq) for seq in itertools.product("01", repeat=amount_of_zero_rows)]
    for seq in combination:
        counter  = 0
        for row in zero_rows:
            K_new = K.copy()
            K_new[row] = int(seq[counter])
            counter = counter + 1
        Ks.append(K_new)
    Solutions_binary = []
    Solutions_int = []
    Solutions_hex = []
    for Kcur in Ks:
        solution_temp = ((np.linalg.inv(T) % 2) @ Kcur) %2
        solution = '0b'
        for value in solution_temp:
            solution = solution + str(int(value[0]))
        Solutions_binary.append(solution)
        soultion_int = int(solution,2)
        Solutions_int.append(soultion_int)
        Solutions_hex.append(hex(soultion_int))
    return Solutions_binary,Solutions_int,Solutions_hex

def estimate_xorin(crc_algorithm,estimated_poly_deg):
    print('\n')
    print('Estimating xor in value of crc code:')
    print('Creating a basis of independet componenets, each byte array has value 2^i, where i = 0 to n - 1 (n = polynomial degree)\n')
    ls = []
    for i in range(estimated_poly_deg):
        cur_val = bytearray(long_to_bytes(1<<i,estimated_poly_deg//8)) # creates powers of 2 from 1 to 2^(estimated_poly_deg-1)
        ls.append(cur_val)
    ls_binary_differntial = []
    for i in range(estimated_poly_deg):
        cur_bin = bin(differential_message(ls[(i) % estimated_poly_deg],ls[(i+1) % estimated_poly_deg],crc_algorithm,False))[2:]
        cur_bin = (estimated_poly_deg-len(cur_bin))*'0' + cur_bin
        ls_binary_differntial.append(cur_bin)
    T = np.zeros((estimated_poly_deg,estimated_poly_deg),np.uint64)
    for i in range(estimated_poly_deg):
        for j in range(estimated_poly_deg):
            T[j,i] = int(ls_binary_differntial[i][j]) # elements of binary string string must be columns
    intital_bin1 = ls[-2]
    intital_bin2 = ls[-1]
    bin_string = bin(differential_message(intital_bin1,intital_bin2,crc_algorithm) ^ calculate_and_print_result(byte_xor(intital_bin1,intital_bin2),crc_algorithm))[2:]
    bin_string = (estimated_poly_deg-len(bin_string))*'0' + bin_string
    K = np.zeros((estimated_poly_deg,1),np.uint64)
    for i in range(estimated_poly_deg):
        K[i] = int(bin_string[i])
    Solutions_binary,Solutions_int,Solutions_hex = solve_system_of_equations_over_gf2(T,K)
    print('Found possible solutions: \n')
    print('Binary form: ' + str(Solutions_binary))
    print('Intger form: ' + str(Solutions_int))
    print('Hex form: ' + str(Solutions_hex))
    return Solutions_binary,Solutions_int,Solutions_hex
    
def print_actual_crc_parameters(params):
    # Pritnting actual CRC parameters
    poly_known_order = params['width']
    print('\n')
    print('----------------------------------------\n')
    print('Actual CRC parameters as described in CRC-engine (taken from wikipedia):')
    print('Actual Polynomial name: ' +  params['name'])
    print('Normal mode: ' + str(hex(params['poly'])))
    print('Reverse mode: ' + str(hex(reverse_poly(params['poly'],poly_known_order))))
    print('Recipolar mode: ' + str(hex(recipolar_poly(params['poly'],poly_known_order))))
    print('Reversed recipolar mode: ' + str(hex(reverse_recipolar_poly(params['poly'],poly_known_order))))
    print('Actual polynomial degree: ' + str(poly_known_order) + '\n')
    print('----------------------------------------\n')
    
    
# %% Main

if __name__ == '__main__':
    print('\n\n')
    print('----------------------------------------\n')
    print('Cyclic redundancy check (CRC) reverse engneering tool.\n')
    print('----------------------------------------\n')
    print('\n')
    print('Choose one of the following choices and write its name below:')
    print(list(crcengine.algorithms_available()))
    while True:
        try:
            crc_algorithm_name = input('Write the name of the CRC code you want to reverse. \n\n')
            crc_algorithm = crcengine.new(crc_algorithm_name)
            break
        except:
            print('\n')
            print('Plese write the name of the algorithm correctly!\n\n')
    params = print_crc_parameters(crc_algorithm_name)
    estimated_poly_normal,estimated_poly_reverse,estimated_poly_recipolar,estimated_poly_recipolar_reverese,estimated_poly_deg = guess_poly(crc_algorithm)
    print_actual_crc_parameters(params)
    xorin_binary,xorin_int,xorin_hex = estimate_xorin(crc_algorithm,estimated_poly_deg)
    
    
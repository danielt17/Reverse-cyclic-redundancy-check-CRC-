# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 17:51:57 2022

@author: danie
"""


# %% Imports

import crcengine 
import numpy as np

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
    return params

def calculate_and_print_result(input_string,crc_algorithm,enb_text=False):
    result = crc_algorithm(input_string)
    if enb_text == True:
        print('Input string: ' + str(input_string) + '\n')
        print('CRC int = ' + str(result) + '. Hex = 0x{:08x}'.format(result) + '\n')
    return result

def differential_message(str1,str2,crc_algorithm):
    # str1 and str2 are bytearray inputs
    # print('We compute a differential (homogenous) message, removing XorIn and XorOut from the equation')
    # C1 + C2 = (T^n(I) + D1 + F) + (T^n(I) + D2 + F) =	D1 + D2 (+ = XOR = addition in GF(2))
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
    estimated_poly_normal = reverse_poly(estimated_poly_reverse,len(bin(estimated_poly_reverse)[2:]))
    print('\n')
    print('----------------------------------------\n')
    print('Estimated CRC polynomial:')
    print('Normal mode: ' + str(hex(estimated_poly_normal)))
    print('Reverse mode: ' + str(hex(estimated_poly_reverse)) + '\n')
    print('----------------------------------------\n')
    return estimated_poly_normal,estimated_poly_reverse
    
# %% Main

if __name__ == '__main__':
    print('\n\n')
    print('----------------------------------------\n')
    print('Cyclic redundancy check (CRC) reverse engneering tool.\n')
    print('----------------------------------------\n')
    print('\n')
    print('Choose one of the following choices and write its name below:')
    print(list(crcengine.algorithms_available()))
    crc_algorithm_name = input('Write the name of the CRC code you want to reverse. \n\n')
    crc_algorithm = crcengine.new(crc_algorithm_name)
    params = print_crc_parameters(crc_algorithm_name)
    estimated_poly_normal,estimated_poly_reverse = guess_poly(crc_algorithm)
    poly_known_order = params['width']
    print('The normal\\reversed\\recipolar\\revered recipolar polynomial representations of ' + params['name'] + ' as defined in CRC-engine (taken from wikipedia): ' + hex(params['poly']) + '\\' + hex(reverse_poly(params['poly'],poly_known_order))  + '\\' + hex(recipolar_poly(params['poly'],poly_known_order)) + '\\' + hex(reverse_recipolar_poly(params['poly'],poly_known_order)) + '.\n')

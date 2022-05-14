# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:19:29 2022

@author: DanielT17
"""

# %% Imports


from collections import Counter
from math import ceil
import numpy as np

# %% Functions

def swap(a,b):
    '''
    Description: 
        This function swaps two variables.
    Inputs:
        a,b - ints.
    Outputs:
        c,d - ints.
    '''
    c = b
    d = a
    return c,d

def bitstring_to_bytes(s,endian='big'):
    '''
    Description: 
        This function gets a bit string binary and turns it to bytes array.
    Inputs:
        s - string - binary string.
        endian - str - big or little endian representation
    Outputs:
        return - byte array of s.
    '''
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder=endian)

def bytearray_to_int(s,endian="big"):
    '''
    Description: 
        This function turn a byte array into an int.
    Inputs:
        s - byte array.
    Outputs:
        returns - int.
    '''
    return int.from_bytes(s, endian)

def int_to_bytearray(s,endian="big"):
    '''
    Description: 
        This function turns an int into a bytearray.
    Inputs:
        s - int.
    Outputs:
        returns - byte array.
    '''
    return s.to_bytes(ceil(s.bit_length()/8),endian)

def remove_zeros_from_binary_string(string):
    '''
    Description: 
        This function removes preappended zeros to a binary string.
    Inputs:
        string - a string sequence of ones and zeros.
    Outputs:
        string - without preappended zeros.
    '''
    counter = 0
    for char in string:
        if char == '0':
            counter += 1
        else:
            break
    return string[counter:]

def turn_bitstring_to_numpy_array_of_bits(string,crc_width):
    '''
    Description:
        This function turns a bit string into a numpy array of size crc_width
        where each arr[i] is equal to string[i]. A binary vector in GF(2).
    Inputs:
        string - string - a binary string.
        crc_width - int - the crc polynomial width
    Outputs:
        arr - numpy array - vector version of the binary string in GF(2).
    '''
    arr = np.zeros((1,crc_width),dtype=np.uint8)
    for i in range(crc_width):
        arr[0,i] = int(string[i])
    return arr

def turn_numpy_array_of_bits_to_bitstring(arr,crc_width):
    '''
    Description:
        This function turns a numpy array of bits in GF(2) to a bit string.
    Inputs:
        arr - numpy array - a vector of bits in GF(2).
        crc_width - int - the crc polynomial width
    Outputs:
        string - string - a binary string.
    '''
    string = ''
    for i in range(crc_width):
        string += str(arr[i])
    return string

def byte_xor(ba1, ba2):
    """
    Description:
        This function computes the xor between two byte arrays.
    Inputs:
        ba1, ba2 - byte arrays - are byte arrays of the same size to be xored.
    Outputs:
        xored - byte array - A byte array with the xored result.
    """
    xored = bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
    return xored

def unique(ls,version=0):
    '''
    Description:
        This function find unique elemnts in a list, created because numpy
        unique functionality discards string when using unique.
    Inputs:
        ls - list - list to be uniqued.
        version - int - type of unique method.
    Outputs:
        unique_list - list - list of unique elements.
    '''
    if version == 0:
        unique_list = Counter(ls).keys()
        counts = Counter(ls).values()
        return list(unique_list),list(counts)
    elif version == 1:
        unique_list = []
        for x in ls:
            if x not in unique_list:
                unique_list.append(x)
        return unique_list






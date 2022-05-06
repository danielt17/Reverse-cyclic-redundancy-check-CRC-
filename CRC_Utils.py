# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:23:20 2022

@author: DanielT17
"""

# %% Imports

from crcengine import get_algorithm_params
from math import ceil

# %% Functions

def Print_Crc_Parameters(crc_algorithm_name):
    '''
    Description:
        This functions returns crc algorithm parameters.
    Inputs:
        crc_algorithm_name - str - the name of the crc algorithm.
    Outputs:
        None. Prints text.
    '''
    params = get_algorithm_params(crc_algorithm_name)
    print('\nCyclic redundancy check parameters: \n')
    for _,param in enumerate(params.items()):
        if param[0] == 'poly':
            print('poly: ' + str(hex(param[1])))
        else:
            print(str(param[0]) + ': ' + str(param[1]) + '.')
    print('\n')
    return params['width']

def Get_CRC(data,crc_algorithm):
    '''
    Description:
        This functions computes the crc of some byte array named data, and returns
        a byte array object named crc_bytes.
    Inputs:
        data - byte array - we want to calculate the crc of this input.
        crc_algorithm - crcengine.calc._CrcLsbf - the crc object which will be
        used for the calculation.
    Outputs:
        crc_bytes - byte array - the byte array of object of the resulting crc.
    '''
    crc = crc_algorithm(data)
    length_in_bits = crc.bit_length()
    crc_bytes = crc.to_bytes(ceil(length_in_bits/8),'big')
    return crc_bytes

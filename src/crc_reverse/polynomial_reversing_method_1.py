# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:39:50 2022

@author: DanielT17
"""

# %% Imports

from .utils import byte_xor,bytearray_to_int
from .polynomial_utils import ranking_estimated_polynomial
from typing import Any

# %% Functions

PacketPair = list[bytes]


def differential_message(crc1: bytes, crc2: bytes) -> bytes:
    '''
    Description:
        This function computes a differential or in another name homogenous message,
        removing XorIn and XorOut from the equation. This is can be seen in the equation below:
        C1 + C2 = (T^n(I) + D1 + F) + (T^n(I) + D2 + F) = D1 + D2.
        Where C1 and C2 are the inhomogenous crcs, I representes the XorIn value, T
        represents the shift operator of the CRC, D1 and D2 are the homogenous crcs, F
        is the XorOut value, n is the degree of the crc polynomial, and addition 
        is in GF(2) and equivalent to xor.
    Inputs:
        crc1 and crc2 - byte arrays - crc values to compute the differential off.
    Outputs:
        diff_crc - byte array - differential crc.
    '''
    diff_crc = byte_xor(crc1,crc2)
    return diff_crc

def estimate_poly(diff_crc1: bytes, diff_crc2: bytes, shift_by: int = 1) -> int:
    '''
    Description:
        We need a spanning basis to reverse the polynomial of the crc therefore
        diff_crc are the differntial message (Homgenous) output of the differntial message algorithm
        such that CRC(2^n) and CRC(2^(n+1)) are used to get the polynomial charateristic.
    Inputs:
        diff_crc1,diff_crc2 - byte arrays - differntial crc messages.
    Outputs:
        returns a hex represenation of the polynomial coefficents.
    '''
    diff_crc1_int = bytearray_to_int(diff_crc1);
    diff_crc2_int = bytearray_to_int(diff_crc2);
    if diff_crc1_int >= diff_crc2_int:
        poly = (diff_crc2_int>>shift_by)^diff_crc1_int
    else:
        poly = (diff_crc1_int>>shift_by)^diff_crc2_int
    return poly

def full_process_estimating_poly(crc1: bytes, crc2: bytes, crc3: bytes, crc4: bytes) -> int:
    '''
    Description:
        This function gets 4 crcs of equal size and estimates the crcs polynomial
        coefficents.
    Inputs:
        crc1,crc2,crc3,crc4 - byte arays - byte arrays of crcs.
    Outputs:
        poly - int - estimated polynimial.
    '''
    diff_crc1 = differential_message(crc1,crc2)
    diff_crc2 = differential_message(crc3,crc4)
    poly = estimate_poly(diff_crc1,diff_crc2)
    return poly

def estimate_poly_over_all_packets_method_1(first_step_packets: list[PacketPair], crc_width: int) -> tuple[list[int], Any]:
    '''
    Description:
        This function estimated the polynomial over all the given first step packets
        given by the user using Xor shift method.
    Inputs:
        first_step_packets - A list of lists with a combination of data + crc.
        crc_width - int - estimated polynomial degree.
    Outputs:
        poly - int - estimated polynimial.
    '''
    print('\n\n')
    print('-------------------------------------------------')
    print('Estimating using method 1 (Xor-shift method):')
    print('-------------------------------------------------')
    print('\n')
    polys = []
    amount_of_quads = len(first_step_packets)//2 - 1
    for i in range(amount_of_quads):
        poly = full_process_estimating_poly(first_step_packets[2*i][1],first_step_packets[2*i+1][1],first_step_packets[2*i+2][1],first_step_packets[2*i+3][1])
        if poly >= 2**(crc_width):
            continue
        polys.append(poly)
    polys_best,occurrence = ranking_estimated_polynomial(polys)
    return polys_best,occurrence

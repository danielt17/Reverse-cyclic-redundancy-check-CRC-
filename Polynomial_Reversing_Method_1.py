# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:39:50 2022

@author: DanielT17
"""

# %% Imports

from Utils import Byte_Xor,Bytearray_To_Int
from Polynomial_Utils import Ranking_Estimated_Polynomial

# %% Functions

def Differential_Message(crc1,crc2):
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
    diff_crc = Byte_Xor(crc1,crc2)
    return diff_crc

def Estimate_Poly(diff_crc1,diff_crc2,shift_by=1):
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
    diff_crc1_int = Bytearray_To_Int(diff_crc1);
    diff_crc2_int = Bytearray_To_Int(diff_crc2);
    if diff_crc1_int >= diff_crc2_int:
        poly = (diff_crc2_int>>shift_by)^diff_crc1_int
    else:
        poly = (diff_crc1_int>>shift_by)^diff_crc2_int
    return poly

def Full_Process_Estimating_Poly(crc1,crc2,crc3,crc4):
    '''
    Description:
        This function gets 4 crcs of equal size and estimates the crcs polynomial
        coefficents.
    Inputs:
        crc1,crc2,crc3,crc4 - byte arays - byte arrays of crcs.
    Outputs:
        poly - int - estimated polynimial.
    '''
    diff_crc1 = Differential_Message(crc1,crc2)
    diff_crc2 = Differential_Message(crc3,crc4)
    poly = Estimate_Poly(diff_crc1,diff_crc2)
    return poly

def Estimate_Poly_Over_All_Packets_Method_1(first_step_packets,crc_width):
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
        poly = Full_Process_Estimating_Poly(first_step_packets[2*i][1],first_step_packets[2*i+1][1],first_step_packets[2*i+2][1],first_step_packets[2*i+3][1])
        if poly >= 2**(crc_width):
            continue
        polys.append(poly)
    polys_best,occurrence = Ranking_Estimated_Polynomial(polys)
    return polys_best,occurrence
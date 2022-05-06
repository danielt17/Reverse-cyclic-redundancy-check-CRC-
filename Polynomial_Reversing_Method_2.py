# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:41:20 2022

@author: DanielT17
"""

# %% Imports

from Utils import Swap,Bytearray_To_Int,Int_To_Bytearray,Byte_Xor,Remove_Zeros_From_Binary_String
from Polynomial_Utils import Ranking_Estimated_Polynomial
from math import ceil

# %% Functions

def Poly_Mod(a, b):
    '''
    Description:
        This function calculates the polynomial modulo over GF(2) between two
        polyinomials.
    Inputs:
        a,b - ints - both of the variables are the int represenations of polynomial
        parameters.
    Outputs:
        a - int - modulo of the of one polynomial with respect to the other in GF(2).
    '''
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a

def Poly_GCD(a, b):
    '''
    Description:
        This function computes the GCD between two polynomials over GF(2).
    Inputs:
        a,b - ints - both of the variables are the int represenations of polynomial
        parameters.
    Outputs:
        a - int - the polynomial GCD over GF(2).
    '''
    if b>a:
        a,b = Swap(a,b)
    while b != 0:
        a, b = b, Poly_Mod(a, b)
    return a

def Packet_Transform_To_Message_Big_Endian_Crc_Little_Endian_Concatenate_Turn_To_Int_Big_Endian(packet):
    '''
    Description:
        This function preprocesses packets into the following represenation
        packet -> int(m(big endian) + crc(little endian)) where int is read as big
        endian.
    Inputs:
        packet - list - a list containing msg and crc pair.
    Outputs:
        packet_int - int - the packets in int representation according to the method.
    '''
    m = packet[0]; r = Bytearray_To_Int(packet[1])
    packet_int = Bytearray_To_Int(m + Int_To_Bytearray(r,'little'))
    return packet_int

def Packet_Concatenate(packet):
    '''
    Description:
        This function preprocesses a packet by concatanting the packet msg and
        crc into a full message and than turning it to big endian int.
    Inputs:
        packet - list - a list containing msg and crc pair.
    Outputs:
        packet_int - int - the packets in int representation according to the method.
    '''
    m = packet[0]; r = packet[1]
    packet_int = Bytearray_To_Int(m + r)
    return packet_int
    
def Pre_Processing_Packets_Method_2(packet1,packet2,packet3,crc_family):
    '''
    Description:
        This function preprocesses three packets into appropraite usage in the
        function Polynomial_Recovery_Gcd_Method.
    Inputs:
        packet1, packet2, packet3 - lists - are lists containing msg and crc pairs.
        crc_family - int - what type of preprocessing should be done.
    Outputs:
        packet1_int,packet2_int,packet3_int - ints - the packets in int representation
        according to the preprocessing method.
    '''
    if crc_family == 0:
        packet1_int = Packet_Transform_To_Message_Big_Endian_Crc_Little_Endian_Concatenate_Turn_To_Int_Big_Endian(packet1)
        packet2_int = Packet_Transform_To_Message_Big_Endian_Crc_Little_Endian_Concatenate_Turn_To_Int_Big_Endian(packet2)
        packet3_int = Packet_Transform_To_Message_Big_Endian_Crc_Little_Endian_Concatenate_Turn_To_Int_Big_Endian(packet3)
    elif crc_family == 1:
        packet1_int = Packet_Concatenate(packet1)
        packet2_int = Packet_Concatenate(packet2)
        packet3_int = Packet_Concatenate(packet3)
    return packet1_int,packet2_int,packet3_int

def Polynomial_Recovery_Gcd_Method(packet1_int,packet2_int,packet3_int,crc_family):
    '''
    Description:
        This function does polynomial recovery from using the GCD from 3 pakcets.
    Inputs:
        packet1_int,packet2_int,packet3_int - ints - with appropriate representation.
        crc_family - int - what type of preprocessing should be done.
    Outputs:
        poly - int - return estimated polynomial (0 for not estimated).
    '''
    if crc_family == 0:
        endian = 'little'
        packet1 = packet1_int.to_bytes(ceil(packet1_int.bit_length()/8),endian)
        packet2 = packet2_int.to_bytes(ceil(packet2_int.bit_length()/8),endian)
        packet3 = packet3_int.to_bytes(ceil(packet3_int.bit_length()/8),endian)
        homogenous_packet1 = bin(Bytearray_To_Int(Byte_Xor(packet1,packet2)))[2:][::-1]
        homogenous_packet2 = bin(Bytearray_To_Int(Byte_Xor(packet1,packet3)))[2:][::-1]
        homogenous_packet1 = Remove_Zeros_From_Binary_String(homogenous_packet1)
        homogenous_packet2 = Remove_Zeros_From_Binary_String(homogenous_packet2)
        try:
            homogenous_packet1 = int(homogenous_packet1,2); homogenous_packet2 = int(homogenous_packet2,2)
        except:
            print("There's a sequence where the same packet happenss twice, not using it.")
            poly = 0 
            return poly
    elif crc_family == 1:
        homogenous_packet1 = packet1_int^packet2_int
        homogenous_packet2 = packet1_int^packet3_int
    poly = Poly_GCD(homogenous_packet2, homogenous_packet1)
    try:
        poly = int(hex(poly)[3:],16)
    except:
        print("The inputed packets don't supply enough information, please supply other packets.\n")
        poly = 0
    return poly
    
def Estimate_Poly_Over_All_Packets_Method_2(first_step_packets,crc_width):
    '''
    Description:
        This function estimated the polynomial over all the given first step packets
        given by the user using GCD method.
    Inputs:
        first_step_packets - list - A list of lists with a combination of data + crc.
        crc_width - int - estimated polynomial degree.
    Outputs:
        poly - int - estimated polynimial.
    '''
    print('\n\n')
    print('--------------------------------------------')
    print('Estimating using method 2 (GCD method):')
    print('--------------------------------------------')
    print('\n')
    polys = []
    amount_of_triplets = len(first_step_packets)-2
    crc_families = [0,1];
    for i in range(amount_of_triplets):
        for crc_family in crc_families:
            packet1_int,packet2_int,packet3_int = Pre_Processing_Packets_Method_2(first_step_packets[i],first_step_packets[i+1],first_step_packets[i+2],crc_family)
            poly = Polynomial_Recovery_Gcd_Method(packet1_int,packet2_int,packet3_int,crc_family)
            if poly >= 2**(crc_width):
                continue
            polys.append(poly)
    polys_best,occurrence = Ranking_Estimated_Polynomial(polys)
    return polys_best,occurrence



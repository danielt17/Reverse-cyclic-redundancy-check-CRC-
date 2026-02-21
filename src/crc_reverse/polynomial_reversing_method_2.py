# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:41:20 2022

@author: DanielT17
"""

# %% Imports

from .utils import swap,bytearray_to_int,int_to_bytearray,byte_xor,remove_zeros_from_binary_string
from .polynomial_utils import ranking_estimated_polynomial
from math import ceil
from typing import Any

# %% Functions

PacketPair = list[bytes]


def poly_mod(a: int, b: int) -> int:
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

def poly_gcd(a: int, b: int) -> int:
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
        a,b = swap(a,b)
    while b != 0:
        a, b = b, poly_mod(a, b)
    return a

def packet_transform_to_message_big_endian_crc_little_endian_concatenate_turn_to_int_big_endian(packet: PacketPair) -> int:
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
    m = packet[0]; r = bytearray_to_int(packet[1])
    packet_int = bytearray_to_int(m + int_to_bytearray(r,'little'))
    return packet_int

def packet_concatenate(packet: PacketPair) -> int:
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
    packet_int = bytearray_to_int(m + r)
    return packet_int
    
def pre_processing_packets_method_2(
    packet1: PacketPair,
    packet2: PacketPair,
    packet3: PacketPair,
    crc_family: int,
) -> tuple[int, int, int]:
    '''
    Description:
        This function preprocesses three packets into appropraite usage in the
        function polynomial_recovery_gcd_method.
    Inputs:
        packet1, packet2, packet3 - lists - are lists containing msg and crc pairs.
        crc_family - int - what type of preprocessing should be done.
    Outputs:
        packet1_int,packet2_int,packet3_int - ints - the packets in int representation
        according to the preprocessing method.
    '''
    if crc_family == 0:
        packet1_int = packet_transform_to_message_big_endian_crc_little_endian_concatenate_turn_to_int_big_endian(packet1)
        packet2_int = packet_transform_to_message_big_endian_crc_little_endian_concatenate_turn_to_int_big_endian(packet2)
        packet3_int = packet_transform_to_message_big_endian_crc_little_endian_concatenate_turn_to_int_big_endian(packet3)
    elif crc_family == 1:
        packet1_int = packet_concatenate(packet1)
        packet2_int = packet_concatenate(packet2)
        packet3_int = packet_concatenate(packet3)
    else:
        raise ValueError("crc_family must be 0 or 1")
    return packet1_int, packet2_int, packet3_int

def polynomial_recovery_gcd_method(packet1_int: int, packet2_int: int, packet3_int: int, crc_family: int) -> int:
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
        homogenous_packet1 = bin(bytearray_to_int(byte_xor(packet1,packet2)))[2:][::-1]
        homogenous_packet2 = bin(bytearray_to_int(byte_xor(packet1,packet3)))[2:][::-1]
        homogenous_packet1 = remove_zeros_from_binary_string(homogenous_packet1)
        homogenous_packet2 = remove_zeros_from_binary_string(homogenous_packet2)
        try:
            homogenous_packet1 = int(homogenous_packet1,2); homogenous_packet2 = int(homogenous_packet2,2)
        except:
            print("There's a sequence where the same packet happenss twice, not using it.")
            poly = 0 
            return poly
    elif crc_family == 1:
        homogenous_packet1 = packet1_int^packet2_int
        homogenous_packet2 = packet1_int^packet3_int
    else:
        raise ValueError("crc_family must be 0 or 1")
    poly = poly_gcd(homogenous_packet2, homogenous_packet1)
    try:
        poly = int(hex(poly)[3:],16)
    except:
        print("The inputed packets don't supply enough information, please supply other packets.\n")
        poly = 0
    return poly
    
def estimate_poly_over_all_packets_method_2(first_step_packets: list[PacketPair], crc_width: int) -> tuple[list[int], Any]:
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
            packet1_int,packet2_int,packet3_int = pre_processing_packets_method_2(first_step_packets[i],first_step_packets[i+1],first_step_packets[i+2],crc_family)
            poly = polynomial_recovery_gcd_method(packet1_int,packet2_int,packet3_int,crc_family)
            if poly >= 2**(crc_width):
                continue
            polys.append(poly)
    polys_best,occurrence = ranking_estimated_polynomial(polys)
    return polys_best,occurrence



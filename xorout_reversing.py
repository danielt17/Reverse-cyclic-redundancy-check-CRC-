# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:49:56 2022

@author: DanielT17
"""

# %% Imports

from crcengine import create
from crc_utils import get_crc
from utils import bytearray_to_int,byte_xor,unique
import numpy as np

# %% Functions

def estimate_xor_out(packet,poly,crc_width,xor_in,ref_in,ref_out):
    '''
    Description:
        This function estimates xor_out given a packet and some parameters about
        the crc algorithm.
    Inputs:
        packet - list - list where the first entry is the message 
        and the second is the crc.
        cur_poly - int - estimated polynomial.
        crc_width - int - the crc polynomial width.
        xor_in - int - estimated xor_in in value.
        ref_in - boolean - flip or not the entry bits.
        ref_out - boolean - flip or not the output bits.
    Outputs:
        xor_out - int - estimated xor_out_value.
    '''
    crc_algorithm = create(poly, crc_width, xor_in, ref_in=ref_in,ref_out=ref_out, xor_out=0)
    crc_estimated = get_crc(packet[0],crc_algorithm)
    xor_out = bytearray_to_int(byte_xor(crc_estimated,packet[1]))
    return xor_out

def estimate_xor_out_all_possiblities(first_step_packets,second_step_packets,generator_polys,useful_xor_in,crc_width):
    '''
    Description:
        This function gets packets, the generator polynomial estimated and the 
        relevant xor in values and returns over them all the most likely xor out
        value, and description of crc parameters.
    Inputs:
        first_step_packets,second_step_packets - lists - list where the first 
        entry is the message and the second is the crc.
        generator_polys - list - list of valid generator polynomials.
        useful_xor_in - list of lists - valid estimated xor_in values with the
        corresponding generator polynomial.
        crc_width - int - the crc polynomial width.
    Outputs:
        combinations - list - a list of the following estimated parameters
        [poly,crc_width,xor_in,ref_in,ref_out,xor_out].
    '''
    ref_ins = [True,False]; ref_outs = [True,False];
    packets = first_step_packets + second_step_packets
    combinations = [];
    threshold = 2 # maximum number of packets which can have a different XorOut value.
    for i in range(len(generator_polys)):
        poly_bin = bin(int(generator_polys[i]))[2:]
        poly_length = len(poly_bin)
        if poly_length > crc_width:
            poly = int(poly_bin[poly_length-crc_width:],2)
        else:
            poly = int(generator_polys[i])
        possible_xor_in = useful_xor_in[i]
        for xor_in in possible_xor_in:
            for ref_in in ref_ins:
                for ref_out in ref_outs:
                    xor_outs = []
                    for packet in packets:
                        xor_out = estimate_xor_out(packet,poly,crc_width,int(xor_in),ref_in,ref_out)
                        xor_outs.append(xor_out)
                    if len(xor_outs) <= np.max(np.unique(xor_outs,return_counts=True)[1]) + threshold:
                        combinations.append([poly,crc_width,int(xor_in),ref_in,ref_out,xor_out])
    combinations = unique(combinations,1)
    return combinations
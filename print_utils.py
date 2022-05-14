# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:25:44 2022

@author: DanielT17
"""

# %% Imports

import numpy as np
from polynomial_utils import generate_all_poly_representations

# %% Functions

def print_packets(packets):
    '''
    Description:
        This function prints packets entered by the user in hexadecimal.
    Inputs:
        packets - list - a list of packets.
    Outputs:
        None. 
        Prints the packets in hexadecimal as inputed by the user.
    '''
    print('\nPresenting packets inputed by user: \n')
    for i in range(len(packets)):
        print('Packet ' + str(i+1) + ': ' + packets[i].hex())
        
def print_all_polynomial_representations(poly,crc_width):
    '''
    Description:
        This function prints all possible polynomial representations. 
    Inputs:
        poly - int - polynomial coefficents
        crc_width - int - polynomial degree
    Outputs:
        None.
        Prints all possible polynomial representations.
    '''
    estimated_reverse_poly,estimated_poly_recipolar,estimated_poly_recipolar_reverese,estimated_reverse_poly_recipolar,estimated_reverse_poly_recipolar_reverese = generate_all_poly_representations(poly,crc_width)
    print('\n')
    print('----------------------------------------')
    print('Estimated CRC polynomial:')
    print('Normal mode:                     ' + str(hex(poly)))
    print('Reverse mode:                    ' + str(hex(estimated_reverse_poly)))
    print('Recipolar mode:                  ' + str(hex(estimated_poly_recipolar)))
    print('Reversed recipolar mode:         ' + str(hex(estimated_poly_recipolar_reverese)))
    print('Recipolar reverse mode:          ' + str(hex(estimated_reverse_poly_recipolar)))
    print('Reversed recipolar reverse mode: ' + str(hex(estimated_reverse_poly_recipolar_reverese)))
    print('----------------------------------------\n')
    
def print_estimated_polynomial_by_ranking_after_method(polys,occurrence,crc_width,enable_pre_text=True):
    '''
    Description:
        This fucntion gets a list of ranking (occurrence) and polynomial and 
        print them in this order. 
    Inputs:
        polys - list - list of possible candidate polynomials.
        occurrence - numpy array - Ordered ranking of the polynomials.
        crc_width - int - estimated polynomial degree
    Outputs:
        None. Prints polynomial in order of ranking.
    '''
    if enable_pre_text:
        print('\n\nPrinting the three most likely polynomials: \n')
    else:
        print('\n\n\n\n\n')
        print('-------------------------------------------------------------------------------------')
        print('The list of polynomials we will continue to use in our XorIn estimation procedure:')
        print('-------------------------------------------------------------------------------------\n\n')
    for i in range(len(polys)):
        print('\nProbability to be the right polynomial is: ' + str(np.round(occurrence[i],2)) + '%.')
        print_all_polynomial_representations(polys[i],crc_width)
    if not enable_pre_text:
        print('\n\n\n\n\n')
        
def print_estimated_polynomials_and_xor_in(generator_polys,useful_polys,useful_xor_in):
    '''
    Description:
        This function gets as input three lists, the generator polynomials, 
        actual estimated polynomial, and estimated XorIns and prints the relvant
        information about them in hex.
    Inputs:
        generator_polys - list - a list of valid generator polynomials.
        useful_polys - list - a list of actual polynomials which result in valid,
        xor_in value.
        useful_xor_in - list - a list of possible xor_in values.
    Outputs:
        None. Prints a combination of the generator polynomial, actual polynomial
        and the estiamted XorIn-s.
    '''
    n = len(generator_polys)
    print('------------------------------------------------------------------------------------------------')
    print('Estimated XorIn (seed) values and its relevant generator polynomial, and actual polynomial:')
    print('------------------------------------------------------------------------------------------------')
    print('\n\n')
    useful_xor_in_hex = []
    for i in range(n):
        ls_temp = []
        for j in range(len(useful_xor_in[i])):
            ls_temp.append(hex(int(useful_xor_in[i][j])))
        useful_xor_in_hex.append(ls_temp)
    for i in range(n):
        print('Generator polynomial (taps): ' + hex(generator_polys[i]))
        print('Actual polynomial:           ' + hex(useful_polys[i]))
        print('Estimated XorIn (seed):      ' + str(useful_xor_in_hex[i])[2:-2])
        print('\n\n')
    print('-----------------------------------------------')
    print('\n\n\n')

def print_all_possible_xor_outs(combinations):
    '''
    Description:
        This function prints out combinations of estimated polynomial,XorIn and
        XorOut.
    Inputs:
        combinations - list of lists - list of lists of possible estimated parameters.
    Outputs:
        None. Prints a combination of the generator polynomial, XorIn, and
        XorOut.
    '''
    if len(combinations) == 0:
        print('\n\n')
        print('--------------------------------------------------------------')
        print('XorOut estimation algorithm failed! no matching combinations')
        print('--------------------------------------------------------------')
        print('\n\n')
    else:
        print('\n\n')
        print('----------------------------------')
        print('Estimated XorOut combinations:')
        print('----------------------------------')
        print('\n\n')
        for i in range(len(combinations)):
            print('Generator polynomial (taps): ' + hex(combinations[i][0]))
            print('Estimated XorIn (seed):      ' + hex(combinations[i][2]))
            print('Estimated XorOut (Mask/Final):     ' + hex(combinations[i][5]))
            print('\n')
        print('\n\n\n\n\n')

def print_estimated_full_estimated(combinations):
    '''
    Description:
        This function print a crcengine like description of the estimated CRC.
    Inputs:
        combinations - list of lists - list of lists of possible estimated parameters.
    Outputs:
        None. Print crcengine like description of the estimated CRC.
    ''' 
    print('\n\n\n\n\n\n\n\n\n')
    print('-----------------------------------------------')
    print('Results of CRC reverse engneering algorithm:')
    print('-----------------------------------------------')
    if len(combinations) == 0:
        print('\n')
        print('-----------------------------------------------')
        print('CRC reversing algorithm failed!')
        print('-----------------------------------------------')
        print('\n\n\n\n\n\n\n\n')
    else:
        for i in range(len(combinations)):
            print('\n')
            print('-----------------------------------------------')
            print('poly:        ' + hex(combinations[i][0]))
            print('width:       ' + str(combinations[i][1]))
            print('seed:        ' + hex(combinations[i][2]))
            print('ref_in:      ' + str(combinations[i][3]))
            print('ref_out:     ' + str(combinations[i][4]))
            print('xor_out:     ' + hex(combinations[i][5]))
            print('-----------------------------------------------')
        print('\n\n\n\n\n\n\n\n')
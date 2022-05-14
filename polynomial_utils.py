# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:28:39 2022

@author: DanielT17
"""

# %% Imports

import numpy as np
from utils import unique

# %% Functions

def reverse_poly(poly,order):
    '''
    Description:
        Printing reverse polynomial representation.
    Inputs:
        poly - int - polynomial coefficents
        order - int - polynomial degree
    Outputs:
        return - int - reverse polynomial represenation
    '''
    len_string = order - len(bin(poly)[2:])
    return int(bin(poly)[::-1][:-2],2) << len_string

def recipolar_poly(poly,order):
    '''
    Description:
        Printing recipolar polynomial representation: p(x) -> p(x^(-1))*x^n. 
    Inputs:
        poly - int - polynomial coefficents
        order - int - polynomial degree
    Outputs:
        return - int - reverse polynomial represenation
    '''
    temp = bin(poly)[::-1][:-2][1:]
    temp = temp  + '0'*(order-len(temp)-1) + '1'
    return int(temp,2)

def generate_all_poly_representations(poly,crc_width,enb_combinations=False):
    '''
    Description:
        This function calculates all possible polynomial representations. 
    Inputs:
        poly - int - polynomial coefficents
        crc_width - int - polynomial degree
        enb_combinations - boolean - if enabled returns a list of all possible
        polynomil combinations.
    Outputs:
        estimated_reverse_poly,estimated_poly_recipolar,
        estimated_poly_recipolar_reverese,estimated_reverse_poly_recipolar,
        estimated_reverse_poly_recipolar_reverese - ints - polynomial representations.
    '''
    estimated_reverse_poly = reverse_poly(poly,crc_width)
    estimated_poly_recipolar = recipolar_poly(poly,crc_width)
    estimated_poly_recipolar_reverese = reverse_poly(poly,crc_width)
    estimated_reverse_poly_recipolar = recipolar_poly(estimated_reverse_poly,crc_width)
    estimated_reverse_poly_recipolar_reverese = reverse_poly(estimated_poly_recipolar,crc_width)
    if enb_combinations:
        ls = [poly,estimated_reverse_poly,estimated_poly_recipolar,estimated_poly_recipolar_reverese,estimated_reverse_poly_recipolar,estimated_reverse_poly_recipolar_reverese]
        polys = []
        for cur_poly in ls:
            for i in range(4):
                if i == 0:      polys.append(cur_poly)
                elif i == 1:    polys.append(cur_poly+1)
                elif i == 2:    polys.append(cur_poly+2**(crc_width))
                elif i == 3:
                    counter = 0;
                    hex_cur_poly = hex(cur_poly)[2:]
                    for j in reversed(hex_cur_poly):
                        if j == '0':
                            counter += 1
                        else:
                            break;
                    if counter != 0:
                        polys.append(int(hex_cur_poly[:-counter],16))
                        
        return polys
    else:
        return estimated_reverse_poly,estimated_poly_recipolar,estimated_poly_recipolar_reverese,estimated_reverse_poly_recipolar,estimated_reverse_poly_recipolar_reverese
    
def ranking_estimated_polynomial(polys):
    '''
    Description:
        This function gets a list of possible candidate polynomials, and outputs
        the three (or two or one) most likely polynomials. 
    Inputs:
        polys - list - list of intgers which are candidate polynomials.
    Outputs:
        polys_best - list - list of the most likely polynomial to be a correct 
        polynomial, ranked from most likely to least likely.
        occurrence - list - the probability (in this case percentage) of a polynomial
        to be the correct polynomial according to the algorithm.
    '''
    polys = np.asarray(polys,dtype = object)
    polys = polys[polys != 0]
    values, counts = unique(polys)
    for i in reversed(range(3)):
        try: inds = np.argpartition(counts, -(i+1))[-(i+1):]; break;
        except: continue;
    occurrence = []; polys_best = [];
    for ind in inds:
        occurrence.append(counts[ind]); polys_best.append(values[ind]); 
    occurrence = occurrence[::-1]; polys_best = polys_best[::-1]
    occurrence = occurrence/np.sum(occurrence) * 100;
    ranking = np.argsort(occurrence)[::-1]; 
    occurrence = occurrence[ranking];
    polys_best = [x for _,x in sorted(zip(list(ranking),polys_best))][::-1]
    return polys_best,occurrence

def merge_by_ranking_polynomials(occurrence1,polys1,occurrence2,polys2):
    '''
    Description:
        This function gets 2 lists of polynomial and two lists of there respective
        ranking, merges and rescores them with respect to unique values. 
    Inputs:
        occurrence1,occurrence2 - numpy arrays - Ordered ranking of the polynomials.
        polys1,polys2 - numpy arrays - A numpy array of the ordered polynomials.
    Outputs:
        polys_unique - list - list of the remaining ranked unique polynomials.
        new_occurrences - numpy array - array of the ranking of the polynomials.
    '''
    occurrences = np.array(list(occurrence1) + list(occurrence2));
    occurrences = occurrences/np.sum(occurrences)*100
    ranking = np.argsort(occurrences)
    occurrences = list(occurrences[ranking])[::-1]
    polys = list(polys1) + list(polys2)
    polys = [x for _,x in sorted(zip(list(ranking),polys))][::-1]
    polys_unique,_ = unique(polys)
    new_occurrences = [];
    for cur_poly in polys_unique:
        indcies = np.where(cur_poly == np.array(polys))[0]
        temp_occurrence = 0
        for i in indcies:
            temp_occurrence += occurrences[i]
        new_occurrences.append(temp_occurrence)
    new_occurrences = np.array(new_occurrences);  ranking_new = np.argsort(new_occurrences)
    new_occurrences = new_occurrences[ranking_new][::-1]; 
    polys_unique = [x for _,x in sorted(zip(list(ranking_new),polys_unique))][::-1]
    new_occurrences = list(new_occurrences)
    return polys_unique,new_occurrences

def create_valid_unequal_packet_combinations(second_step_packets):
    '''
    Description:
        Create a valid packet combinations to run the XorIn estimation algorithm 
        on.
    Inputs:
        second_step_packets - list - a list of pacekts.
    Outputs:
        packet_combinations - list of lists of lists - a list of valid packet1
        and packet2 combinations of unequal length.
    '''
    num_of_packets = len(second_step_packets)
    packet_combinations = [];
    for i in range(num_of_packets):
        for j in range(num_of_packets):
            packet1 = second_step_packets[i]; packet2 = second_step_packets[j];
            if packet1 == packet2 or j<i:
                continue
            else:
                packet_combinations.append([packet1,packet2])
    return packet_combinations
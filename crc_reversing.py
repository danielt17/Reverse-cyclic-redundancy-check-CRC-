# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:16:10 2022

@author: DanielT17
"""

# %% Imports

from logger_object import logger_object
from ui_functions import start_program
from preprocessing import preprocessing
from utils import unique
from polynomial_utils import merge_by_ranking_polynomials
from print_utils import print_estimated_polynomials_and_xor_in,print_all_possible_xor_outs,print_estimated_full_estimated,print_estimated_polynomial_by_ranking_after_method
from polynomial_reversing_method_1 import estimate_poly_over_all_packets_method_1
from polynomial_reversing_method_2 import estimate_poly_over_all_packets_method_2
from xorin_reversing import estimate_xor_in_all_possiblities
from xorout_reversing import estimate_xor_out_all_possiblities


# %% Functions

def crc_reversing():
    logger = logger_object()
    packets,crc_width = start_program(logger)
    first_step_packets,second_step_packets = preprocessing(packets,crc_width)
    polys1,occurrence1 = estimate_poly_over_all_packets_method_1(first_step_packets,crc_width)
    print_estimated_polynomial_by_ranking_after_method(polys1,occurrence1,crc_width)
    polys2,occurrence2 = estimate_poly_over_all_packets_method_2(first_step_packets,crc_width)
    print_estimated_polynomial_by_ranking_after_method(polys2,occurrence2,crc_width)
    polys,occurrence = merge_by_ranking_polynomials(occurrence1,polys1,occurrence2,polys2)
    print_estimated_polynomial_by_ranking_after_method(polys,occurrence,crc_width,False)
    generator_polys,useful_polys,useful_xor_in = estimate_xor_in_all_possiblities(second_step_packets,polys,crc_width)
    print_estimated_polynomials_and_xor_in(generator_polys,useful_polys,useful_xor_in)
    combinations = estimate_xor_out_all_possiblities(first_step_packets,second_step_packets,generator_polys,useful_xor_in,crc_width)
    if len(combinations) == 0:
        combinations2 = estimate_xor_out_all_possiblities(first_step_packets,second_step_packets,useful_polys,useful_xor_in,crc_width)
        combinations = unique(combinations + combinations2,1)
    print_all_possible_xor_outs(combinations)
    print_estimated_full_estimated(combinations)
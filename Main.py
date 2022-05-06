# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:16:10 2022

@author: DanielT17
"""

# %% Imports

from Logger_Object import Logger_Object
from UI_functions import Start_Program
from Preprocessing import Preprocessing
from Utils import Unique
from Polynomial_Utils import Merge_By_Ranking_Polynomials
from Print_Utils import Print_Estimated_Polynomials_And_Xor_In,Print_All_Possible_Xor_Outs,Print_Estimated_Full_Estimated,Print_Estimated_Polynomial_By_Ranking_After_Method
from Polynomial_Reversing_Method_1 import Estimate_Poly_Over_All_Packets_Method_1
from Polynomial_Reversing_Method_2 import Estimate_Poly_Over_All_Packets_Method_2
from XorIn_Reversing import Estimate_Xor_In_All_Possiblities
from XorOut_Reversing import Estimate_Xor_Out_All_Possiblities


# %% Functions

def Main():
    logger = Logger_Object()
    packets,crc_width = Start_Program(logger)
    first_step_packets,second_step_packets = Preprocessing(packets,crc_width)
    polys1,occurrence1 = Estimate_Poly_Over_All_Packets_Method_1(first_step_packets,crc_width)
    Print_Estimated_Polynomial_By_Ranking_After_Method(polys1,occurrence1,crc_width)
    polys2,occurrence2 = Estimate_Poly_Over_All_Packets_Method_2(first_step_packets,crc_width)
    Print_Estimated_Polynomial_By_Ranking_After_Method(polys2,occurrence2,crc_width)
    polys,occurrence = Merge_By_Ranking_Polynomials(occurrence1,polys1,occurrence2,polys2)
    Print_Estimated_Polynomial_By_Ranking_After_Method(polys,occurrence,crc_width,False)
    generator_polys,useful_polys,useful_xor_in = Estimate_Xor_In_All_Possiblities(second_step_packets,polys,crc_width)
    Print_Estimated_Polynomials_And_Xor_In(generator_polys,useful_polys,useful_xor_in)
    combinations = Estimate_Xor_Out_All_Possiblities(first_step_packets,second_step_packets,generator_polys,useful_xor_in,crc_width)
    if len(combinations) == 0:
        combinations2 = Estimate_Xor_Out_All_Possiblities(first_step_packets,second_step_packets,useful_polys,useful_xor_in,crc_width)
        combinations = Unique(combinations + combinations2,1)
    Print_All_Possible_Xor_Outs(combinations)
    Print_Estimated_Full_Estimated(combinations)

# %% Main

if __name__ == '__main__':
    Main()
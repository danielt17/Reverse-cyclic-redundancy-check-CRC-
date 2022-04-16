# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 12:41:30 2022

@author: DanielT17
"""

# %% Imports

import crcengine 
import numpy as np
import logging
from math import ceil

# %% Formatter

class Custom_Formatter(logging.Formatter):
    """
    Description:
        This function configurates the logger object.
    Inputs:
        logging.Formatter - logging - logging foramatter.
    Outputs:
        formatter.format(record) - formatter - recorded dictionary turns it to string.
    """
    grey = "\x1b[38;20m"; green = "\x1b[32;1m"; yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"; bold_red = "\x1b[31;1m"; reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    FORMATS = {logging.DEBUG: grey + format + reset, 
               logging.INFO: green + format + reset, 
               logging.WARNING: yellow + format + reset, 
               logging.ERROR: red + format + reset, 
               logging.CRITICAL: bold_red + format + reset}

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def Logger_Object():
    """
    Description:
        This function creates and configurates the logger object.
    Inputs:
        None.
    Outputs:
        logger - logging module - a logging object configured.
    """
    logger = logging.getLogger("CRC reversing")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(Custom_Formatter())
    logger.addHandler(ch)
    return logger

# %% Helper functions

def Bitstring_To_Bytes(s):
    '''
    Description: 
        This function gets a bit string binary and turns it to bytes array.
    Inputs:
        s - string - binary string.
    Outputs:
        return - byte array of s.
    '''
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def Bytearray_To_Int(s):
    '''
    Description: 
        This function turn a byte array into an int.
    Inputs:
        s - byte array.
    Outputs:
        returns - int.
    '''
    return int.from_bytes(s, "big")
    

def Byte_Xor(ba1, ba2):
    """
    Description:
        This function computes the xor between two byte arrays.
    Inputs:
        ba1, ba2 - byte arrays - are byte arrays of the same size to be xored.
    Outputs:
        xored - byte array - A byte array with the xored result.
    """
    xored = bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
    return xored

def Print_Crc_Parameters(crc_algorithm_name):
    '''
    Description:
        This functions returns crc algorithm parameters.
    Inputs:
        crc_algorithm_name - str - the name of the crc algorithm.
    Outputs:
        None. Prints text.
    '''
    params = crcengine.get_algorithm_params(crc_algorithm_name)
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

def Print_Packets(packets):
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

def Print_All_Polynomial_Representations(poly,crc_width):
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
    estimated_reverse_poly = reverse_poly(poly,crc_width)
    estimated_poly_recipolar = recipolar_poly(estimated_reverse_poly,crc_width)
    estimated_poly_recipolar_reverese = reverse_poly(estimated_poly_recipolar,crc_width)
    print('\n')
    print('----------------------------------------\n')
    print('Estimated CRC polynomial:')
    print('Normal mode: ' + str(hex(poly)))
    print('Reverse mode: ' + str(hex(estimated_reverse_poly)))
    print('Recipolar mode: ' + str(hex(estimated_poly_recipolar)))
    print('Reversed recipolar mode: ' + str(hex(estimated_poly_recipolar_reverese)))
    print('----------------------------------------\n')
    

# %% User interaction functions

def Print_Start_Program_Text():
    '''
    Description: 
        This function prints the entery text to the program.
    Inputs:
        None.
    Outputs:
        None. 
        prints text.
    '''
    print('\n\n')
    print('----------------------------------------\n')
    print('Cyclic redundancy check (CRC) reverse engneering tool.\n')
    print('----------------------------------------\n')
    print('\n')
    print('There are two modes of running the tool: example mode, by choosing'\
          ' some known CRC with its full parameters, or user mode in which the'\
          ' user eneters his own packet with data and CRC values concatenated.\n')

def Choose_Program_Mode():
    '''
    Description: 
        This function waits for user input which tell it at what mode
        The reversing tool should work (example mode or user mode).
    Inputs:
        None
    Outputs:
        int(program_mode) - int - 1 describing example mode, 2 describing user mode.
    '''
    while True:
        program_mode = input('To enter example mode press 1, for user mode press 2.\n')
        if program_mode == "1": print('\nYou choose: example mode.\n'); break            
        elif program_mode == "2": print('\nYou choose: user mode.\n'); break
        else: print('\nPlease enter either: 1 - example mode, 2 - user mode.\n')
    return int(program_mode)

def Create_Example_Mode_Data(crc_algorithm,hand_crafted = True):
    '''
    Description:
        This function holds the actual examples for example mode..
    Inputs:
        crc_algorithm - crcengine.calc._CrcLsbf - the crc object which will be
        used for the calculation.
        hand_crafted - boolean - either simple examples, or hard real example.
    Outputs:
        packets - list - a list of packets with data + crc at the end.
        crc_width - int - the length of the crc polynomial.
    '''
    print('\nSimulated packet structure:')
    print('Preamble + Sync + Type + DST Address + SRC Address + Sequence Number + Data + CRC\n')
    if not hand_crafted:
        preamble_header = bytearray([170,170])
        sync_header     = bytearray([154,125])
        type_header     = bytearray([0,1])
        dst_address     = bytearray([27,96])
        src_address     = bytearray([120,226])
        data            = bytearray([5,10])
        packet_header = preamble_header + sync_header + type_header + dst_address + src_address
        packets = []
        for i in range(8):
            sequence_number = bytearray([0,i+1])
            packet = packet_header + sequence_number + data
            crc = Get_CRC(packet,crc_algorithm)
            packet = packet + crc
            packets.append(packet)
    else:
        packet1 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10]);    packet1 += Get_CRC(packet1,crc_algorithm);
        packet2 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8]);     packet2 += Get_CRC(packet2,crc_algorithm);
        packet3 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8]);     packet3 += Get_CRC(packet3,crc_algorithm);
        packet4 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12]);    packet4 += Get_CRC(packet4,crc_algorithm);
        packet5 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10]);    packet5 += Get_CRC(packet5,crc_algorithm);
        packet6 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8]);     packet6 += Get_CRC(packet6,crc_algorithm);
        packet7 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,24]);    packet7 += Get_CRC(packet7,crc_algorithm);
        packet8 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8]);     packet8 += Get_CRC(packet8,crc_algorithm);
        packet9 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12]);    packet9 += Get_CRC(packet9,crc_algorithm);
        packet10 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4]);     packet10 += Get_CRC(packet10,crc_algorithm);
        packet11 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,24]);    packet11 += Get_CRC(packet11,crc_algorithm);
        packet12 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8]);     packet12 += Get_CRC(packet12,crc_algorithm);
        packet13 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12]);    packet13 += Get_CRC(packet13,crc_algorithm);
        packet14 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4]);     packet14 += Get_CRC(packet14,crc_algorithm);
        packet15 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,24]);    packet15 += Get_CRC(packet15,crc_algorithm);
        packet16 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8]);     packet16 += Get_CRC(packet16,crc_algorithm);
        
        packets = [packet1,packet2,packet3,packet4,packet5,packet6,packet7,packet8,packet9,packet10,packet11,packet12,packet13,packet14,packet15,packet16]
    Print_Packets(packets)
    return packets

def Get_Initial_Example_Mode_data():
    '''
    Description:
        This function creates packets in example mode, for a given crc algorithm.
    Inputs:
        None.
    Outputs:
        packets - list - a list of packets with data + crc at the end.
        crc_width - int - the length of the crc polynomial.
    '''
    print('Choose one of the following choices and write its name below:\n')
    print(list(crcengine.algorithms_available()))
    while True:
        try:
            crc_algorithm_name = input('Write the name of the CRC code you want to reverse. \n\n')
            crc_algorithm = crcengine.new(crc_algorithm_name)
            break
        except:
            print("\nPlese write the name of the algorithm correctly!\n\n")      
    crc_width = Print_Crc_Parameters(crc_algorithm_name)
    packets = Create_Example_Mode_Data(crc_algorithm,hand_crafted = True)
    return packets,crc_width

def Check_Data_Input(packet,input_type,logger):
    '''
    Description:
        This function gets a packet and input type (binary or hexadecimal) and
        returns whither or not the packet is of the input type.
    Inputs:
        packet - string - a packet input by the user.
    Outputs:
        input_type - str - binary or hexadecimal
    '''
    binary_dict = ['0','1']
    hexadecimal_dict = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
    for num in packet:
        if input_type == 'binary':
            if not num in binary_dict: 
                return False    
        elif input_type == 'hex':
            if not num in hexadecimal_dict:
                return False
        else:
            raise Exception(logger.critical("Cirtical path should not reach this."))
    return True
            

def Get_Initial_User_Mode_data(logger):
    '''
    Description:
        This function get packets in user mode, while interacting with the user
        for different sets of information.
    Inputs:
        loggere - logger object.
    Outputs:
        packets - list - a list of packets with data + crc at the end.
        crc_width - int - the length of the crc polynomial.
    '''
    lower_degree_limit = 8; upper_degree_limit = 128;
    while True:
        crc_width = input('Please write the CRC polynomial degree, a number between 8-128 including the limits: \n')
        try:
            crc_width = int(crc_width)
            if lower_degree_limit <= crc_width <= upper_degree_limit:
                break
            else:
                print('Enter a degree between: ' + str(lower_degree_limit) + ' and ' + str(upper_degree_limit) + '\n')
        except:
            print('The input is not an int, make sure you enter an int.\n')
    min_num_packets = 6; max_num_packets = 100;
    while True:
        number_of_packets = input('Please enter the number of packets you want to enter, while the minimum number of packets is: ' + str(min_num_packets) + ' and the maximum is: ' + str(max_num_packets) +  ' including the limits.\n')
        try:
            number_of_packets = int(number_of_packets)
            if min_num_packets <= number_of_packets <= max_num_packets:
                break
            else:
                print('The number of packets should be in between the limits: ' + str(min_num_packets) + ' and ' + str(max_num_packets) + '.\n')
        except:
            print('The input is not an int, make sure you enter an int.\n')
    while True:
        data_type = input('Before entering your data please choose the representation you want to use: binary or hex. To choose binary write binary, to choose hexadecimal write hex.\n')
        if data_type == 'binary':
            print('\nBinary')
            break
        elif data_type == 'hex':
            print('\nHexadecimal')
            break;
        else:
            print("\nPlease write a correct representation either: binary or hex!\n\n")  
    print('When enetering packets start with the data, and than concatenate the crc.\n')
    print('Enter packets of equal length\n')
    packets = []
    for i in range(number_of_packets):
        if i == ceil(number_of_packets/1.5):
            print('\nEnter packets of unequal length\n')
        while True:
                if data_type == 'binary':
                    packet = input('Enter you packet in binary: ').lower()
                else:
                    packet = input('Enter you packet in hexadecimal: ').lower()
                try:
                    if Check_Data_Input(packet,data_type,logger):
                        if data_type == 'binary':
                            packets.append(Bitstring_To_Bytes(packet))
                        elif data_type == 'hex':
                            packets.append(bytes.fromhex(packet))
                        break
                    else:
                        print('Please enter the data in the following represesntation: ' + data_type + '.\n')
                except:
                    print('Please enter a packet with length bigger than one.')
    Print_Packets(packets)
    return packets,crc_width

def Get_Initial_Data(program_mode,logger):
    '''
    Description:
        This function gets the program_mode and creates a list of data+crc.
    Inputs:
        program_mode - int - choose program mode with respect to user input.
    Outputs:
        data_and_crcs - list - of combinations of data and crcs
    '''
    if program_mode == 1:
        packets,crc_width = Get_Initial_Example_Mode_data()
        
    elif program_mode == 2:
        packets,crc_width = Get_Initial_User_Mode_data(logger)
    else:
        raise Exception(logger.critical("Cirtical path should not reach this."))
    return packets,crc_width

def Start_Program(logger):
    '''
    Description:
        This function starts the run of the CRC reversing tool, collects the user
        data, and output the packets and the crc width of the crc we want to reverse.
    Inputs:
        logger - logger object.
    Outputs:
        packets - list - a list of packets.
        crc_width - int - length or degree of the crc.
    '''
    Print_Start_Program_Text()
    program_mode = Choose_Program_Mode()
    packets,crc_width = Get_Initial_Data(program_mode,logger)
    return packets,crc_width

# %% Preprocessing

def Preprocessing(packets,crc_width):
    '''
    Description:
        This function preprocess the data by spliting the packets list into packet 
        and crc combination by using crc_width parameter, the new sub lists are 
        made of byte arrays.
    Inputs:
        packets - list - a list of packets
        crc_width - int - length or degree of the crc.
    Outputs:
        first_step_packets - a list of lists of packets of equal length
        second_step_packets - a list of lists of packets of unequal length
    '''
    new_packets = []
    for packet in packets:
        cur_packet = packet[:-crc_width//8];  cur_crc = packet[-crc_width//8:]
        packet_crc_pair = [cur_packet,cur_crc]
        new_packets.append(packet_crc_pair)
    num_packets = len(new_packets)
    first_step_packets_num = ceil(num_packets/1.5)
    if first_step_packets_num % 2 == 1:
        first_step_packets_num = first_step_packets_num - 1
    first_step_packets      =   new_packets[:first_step_packets_num]
    second_step_packets     =   new_packets[first_step_packets_num+1:]
    return first_step_packets,second_step_packets

# %% Reversing CRC - Part 1 - Estimating the polynomial

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

def Estimate_Poly(diff_crc1,diff_crc2):
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
        poly = (diff_crc2_int>>1)^diff_crc1_int
    else:
        poly = (diff_crc1_int>>1)^diff_crc2_int
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

def Estimate_Poly_Over_All_Packets(first_step_packets):
    '''
    Description:
        This function estimated the polynomial over all the given first step packets
        given by the user.
    Inputs:
        first_step_packets - A list of lists with a combination of data + crc.
    Outputs:
        poly - int - estimated polynimial.
    '''
    polys = []
    amount_of_quads = len(first_step_packets)//2 - 1
    for i in range(amount_of_quads):
        poly = Full_Process_Estimating_Poly(first_step_packets[2*i][1],first_step_packets[2*i+1][1],first_step_packets[2*i+2][1],first_step_packets[2*i+3][1])
        polys.append(poly)
    polys = np.asarray(polys,np.uint64)
    polys = polys[polys != 0]
    values, counts = np.unique(polys, return_counts=True)
    ind = np.argmax(counts)
    poly = values[ind]
    return poly
    
# %% Reversing CRC - Part 2 - Estimating XorIn



# %% Main function

def Main():
    logger = Logger_Object()
    packets,crc_width = Start_Program(logger)
    first_step_packets,second_step_packets = Preprocessing(packets,crc_width)
    poly = Estimate_Poly_Over_All_Packets(first_step_packets)
    Print_All_Polynomial_Representations(poly,crc_width)
    
# %% Run main

if __name__ == '__main__':
    Main()
    
    
    
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

def Swap(a,b):
    '''
    Description: 
        This function swaps two variables.
    Inputs:
        a,b - ints.
    Outputs:
        c,d - ints.
    '''
    c = b
    d = a
    return c,d

def Bitstring_To_Bytes(s,endian='big'):
    '''
    Description: 
        This function gets a bit string binary and turns it to bytes array.
    Inputs:
        s - string - binary string.
        endian - str - big or little endian representation
    Outputs:
        return - byte array of s.
    '''
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder=endian)

def Bytearray_To_Int(s,endian="big"):
    '''
    Description: 
        This function turn a byte array into an int.
    Inputs:
        s - byte array.
    Outputs:
        returns - int.
    '''
    return int.from_bytes(s, endian)

def Int_To_Bytearray(s,endian="big"):
    '''
    Description: 
        This function turns an int into a bytearray.
    Inputs:
        s - int.
    Outputs:
        returns - byte array.
    '''
    return s.to_bytes(ceil(s.bit_length()/8),endian)

def Remove_Zeros_From_Binary_String(string):
    '''
    Description: 
        This function removes preappended zeros to a binary string.
    Inputs:
        string - a string sequence of ones and zeros.
    Outputs:
        string - without preappended zeros.
    '''
    counter = 0
    for char in string:
        if char == '0':
            counter += 1
        else:
            break
    return string[counter:]

def Turn_Bitstring_To_Numpy_Array_Of_Bits(string,crc_width):
    '''
    Description:
        This function turns a bit string into a numpy array of size crc_width
        where each arr[i] is equal to string[i]. A binary vector in GF(2).
    Inputs:
        string - string - a binary string.
        crc_width - int - the crc polynomial width
    Outputs:
        arr - numpy array - vector version of the binary string in GF(2).
    '''
    arr = np.zeros((1,crc_width),dtype=np.int64)
    for i in range(crc_width):
        arr[0,i] = int(string[i])
    return arr

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
    estimated_poly_recipolar = recipolar_poly(poly,crc_width)
    estimated_poly_recipolar_reverese = reverse_poly(poly,crc_width)
    estimated_reverse_poly_recipolar = recipolar_poly(estimated_reverse_poly,crc_width)
    estimated_reverse_poly_recipolar_reverese = reverse_poly(estimated_poly_recipolar,crc_width)
    
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
        
        # sequence_numbers = [bytearray([10,0]),bytearray([8,0]),bytearray([8,0]),bytearray([12,0]),
        #                     bytearray([10,0]),bytearray([8,0]),bytearray([24,0]),bytearray([8,0]),
        #                     bytearray([40,0]),bytearray([60,0]),bytearray([50,0]),bytearray([70,0]),
        #                     bytearray([12,0]),bytearray([4,0]),bytearray([24,0]),bytearray([8,0]),
        #                     bytearray([12,0]),bytearray([4,0]),bytearray([24,0])]
        
        sequence_numbers = [bytearray([40,0]),bytearray([60,0]),bytearray([50,0]),bytearray([70,0]),
                            bytearray([80,0]),bytearray([100,0]),bytearray([110,100,0])]
        
        data            = bytearray([5,10])
        packet_header = preamble_header + sync_header + type_header + dst_address + src_address
        packets = []
        for j in range(1):
            for i in range(len(sequence_numbers)):
                if j == 0:
                    sequence_number = sequence_numbers[i]
                elif j == 1:
                    sequence_number = sequence_numbers[i][::-1]
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
        packets = [packet1,packet2,packet3,packet4,packet5,packet6,packet7,packet8,packet9,packet10,packet11,packet12,packet13,packet14,packet15]
    Print_Packets(packets)
    return packets

def Get_Initial_Example_Mode_data(hand_crafted=True):
    '''
    Description:
        This function creates packets in example mode, for a given crc algorithm.
    Inputs:
        hand_crafted - boolean - either hand crafted samples or actual packets.
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
    packets = Create_Example_Mode_Data(crc_algorithm,hand_crafted = hand_crafted)
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
    print('Enter packets of equal length, with 1 bit difference, look at packets where only sequence number changes. \n')
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
        packets,crc_width = Get_Initial_Example_Mode_data(hand_crafted=False)
        
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

# %% Reversing CRC - Part 1 - Estimating the polynomial - Method 1

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

def Estimate_Poly_Over_All_Packets_Method_1(first_step_packets):
    '''
    Description:
        This function estimated the polynomial over all the given first step packets
        given by the user using Xor shift method.
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
    try:
        inds = np.argpartition(counts, -3)[-3:] # Three most occuring polynomials
    except:
        try:
            inds = np.argpartition(counts, -2)[-2:] # Two most occuring polynomials
        except:
            inds = np.argpartition(counts, -1)[-1:] # Most occuring polynomial
    occurrence = counts[inds][::-1]; occurrence = occurrence/np.sum(occurrence) * 100;
    polys_best = values[inds][::-1]
    ranking = np.argsort(occurrence)[::-1]; occurrence = occurrence[ranking]; polys_best[ranking]
    return polys_best,occurrence
    
# %% Reversing CRC - Part 1 - Estimating the polynomial - Method 2

def Test_Packets_GCD_Method():
    '''
    Description:
        This function creates test packets for polynomial estimation using method 2.
    Inputs:
        None.
    Outputs:
        packet1_int,packet2_int,packet3_int - ints - packets in int representation
        crc_width - int - polynomial degree we want to estimate.
    '''
    packet1_int = int('aaff00402eec', 16)
    packet2_int = int('aaff00602964', 16)
    packet3_int = int('aaff00502b08', 16)
    crc_width = 16
    return packet1_int,packet2_int,packet3_int,crc_width

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

def Pre_Processing_Packets_Method_2(packet1,packet2,packet3):
    '''
    Description:
        This function preprocesses three packets into appropraite usage in the
        function Polynomial_Recovery_Gcd_Method.
    Inputs:
        packet1, packet2, packet3 - lists - are lists containing msg and crc pairs.
    Outputs:
        packet1_int,packet2_int,packet3_int - ints - the packets in int representation
        according to the preprocessing method.
    '''
    packet1_int = Packet_Transform_To_Message_Big_Endian_Crc_Little_Endian_Concatenate_Turn_To_Int_Big_Endian(packet1)
    packet2_int = Packet_Transform_To_Message_Big_Endian_Crc_Little_Endian_Concatenate_Turn_To_Int_Big_Endian(packet2)
    packet3_int = Packet_Transform_To_Message_Big_Endian_Crc_Little_Endian_Concatenate_Turn_To_Int_Big_Endian(packet3)
    return packet1_int,packet2_int,packet3_int

def Polynomial_Recovery_Gcd_Method(packet1_int,packet2_int,packet3_int):
    '''
    Description:
        This function does polynomial recovery from using the GCD from 3 pakcets.
    Inputs:
        packet1_int,packet2_int,packet3_int - ints - packet represenation in int
        the input should be created such that it is equalivent to the following form:
            1. m (message) in big endian byte array representation.
            2. crc in little endian byte array representation.
            3. concatenate m + crc into one byte array
            4. turn to int in big endian.
    Outputs:
        poly - int - return estimated polynomial (0 for not estimated).
    '''
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
    poly = Poly_GCD(homogenous_packet2, homogenous_packet1)
    try:
        poly = int(hex(poly)[3:],16)
    except:
        print("The inputed packets don't supply enough information, please supply other packets.\n")
        poly = 0
    return poly
    
def Estimate_Poly_Over_All_Packets_Method_2(first_step_packets):
    '''
    Description:
        This function estimated the polynomial over all the given first step packets
        given by the user using GCD method.
    Inputs:
        first_step_packets - A list of lists with a combination of data + crc.
    Outputs:
        poly - int - estimated polynimial.
    '''
    polys = []
    amount_of_triplets = len(first_step_packets)-2
    for i in range(amount_of_triplets):
        packet1_int,packet2_int,packet3_int = Pre_Processing_Packets_Method_2(first_step_packets[i],first_step_packets[i+1],first_step_packets[i+2])
        poly = Polynomial_Recovery_Gcd_Method(packet1_int,packet2_int,packet3_int)
        polys.append(poly)
    polys = np.asarray(polys,np.uint64)
    polys = polys[polys != 0]
    values, counts = np.unique(polys, return_counts=True)
    try:
        inds = np.argpartition(counts, -3)[-3:] # Three most occuring polynomials
    except:
        try:
            inds = np.argpartition(counts, -2)[-2:] # Two most occuring polynomials
        except:
            inds = np.argpartition(counts, -1)[-1:] # Most occuring polynomial
    occurrence = counts[inds][::-1]; occurrence = occurrence/np.sum(occurrence) * 100;
    polys_best = values[inds][::-1];
    ranking = np.argsort(occurrence)[::-1]; occurrence = occurrence[ranking]; polys_best[ranking]
    return polys_best,occurrence
    

# %% Reversing CRC - Part 2 - Estimating XorIn

def Test_Packets_XorIn_Estimation():
    '''
    Description:
        This function creates test packets for XorIn estimation.
    Inputs:
        None.
    Outputs:
        poly - int - estimated polynomial.
        crc_width - int - estimated polynomial degree.
        packet4,packet5 - lists - lists of a combination of message and crc.
    '''
    packet1_int,packet2_int,packet3_int,crc_width = Test_Packets_GCD_Method()
    poly = Polynomial_Recovery_Gcd_Method(packet1_int,packet2_int,packet3_int)
    packet4_hex = 'aaff00402eec'
    packet5_hex = 'aaff040e020450'
    packet4 = bytes.fromhex(packet4_hex)
    packet5 = bytes.fromhex(packet5_hex)
    packet4 = [packet4[:-crc_width//8],packet4[-crc_width//8:]]
    packet5 = [packet5[:-crc_width//8],packet5[-crc_width//8:]]
    return poly,crc_width,packet4,packet5

def Get_Packet_Estimate_Message_Length_Binary(packet):
    '''
    Description:
        This function gets a packet and estimates the message length.
    Inputs:
        packet - list - a list where the first entry is the message and the 
        second is the crc.
    Outputs:
        message_len - int - calculates the length of the message part of the 
        packet.
    '''
    message = packet[0]
    message_len = len(bin(Bytearray_To_Int(message))[2:])
    return message_len

def Build_Relative_Shift_Matrix(l1,l2,poly,crc_width):
    '''
    Description:
        This function creates the following matrix x^k * (x^l1 + x^l2) mod p.
        This matrix is the relative shift matrix which is described in GF(2)
    Inputs:
        l1 - int - length of message one in bits.
        l2 - int - length of message two in bits.
        poly - int - estimated crc polynomial in intger representation.
        crc_width - int - the crc polynomial width
    Outputs:
        matrix - numpy array - A matrix description of the equation above in GF(2).
    '''
    matrix = np.zeros((crc_width,crc_width),dtype=np.int64)
    for k in range(crc_width):
        matrix_row = bin(Poly_Mod((2**(k)) * (2**(l1) + 2**(l2)),poly))[2:]
        matrix_row = '0' * (crc_width-len(matrix_row)) + matrix_row
        matrix[k,:] = Turn_Bitstring_To_Numpy_Array_Of_Bits(matrix_row,crc_width)
    return matrix

def Run_Relative_Shift_Matrix(packet1,packet2,poly,crc_width):
    '''
    Description:
        This function does the relevant preprocessing to calculate the relative
        shift matrix, after being done with the preprocessing it calculates, 
        the relative shift matrix, and returns it.
    Inputs:
        packet1,packet2 - lists - lists where the first entry is the message 
        and the second is the crc.
        poly - int - estimated crc polynomial in intger representation.
        crc_width - int - the crc polynomial width
    Outputs:
        matrix - numpy array - A matrix description of the equation above in GF(2).
    '''
    poly_mat = int('1'+ hex(poly)[2:],16)
    packet1_len = Get_Packet_Estimate_Message_Length_Binary(packet1) 
    packet2_len = Get_Packet_Estimate_Message_Length_Binary(packet2)
    matrix = Build_Relative_Shift_Matrix(packet1_len,packet2_len,poly_mat,crc_width)
    return matrix

# %% Main function

def Main():
    logger = Logger_Object()
    packets,crc_width = Start_Program(logger)
    first_step_packets,second_step_packets = Preprocessing(packets,crc_width)
    print('\n\nEstimating using method 1 (Xor-shift method):\n')
    polys1,occurrence1 = Estimate_Poly_Over_All_Packets_Method_1(first_step_packets)
    print('Printing the three most likely polynomials: \n')
    for i in range(len(polys1)):
        print('\nProbability to be the right polynomial is: ' + str(np.round(occurrence1[i],2)) + '%.')
        Print_All_Polynomial_Representations(polys1[i],crc_width)
    print('\n\nEstimating using method 2 (GCD method):\n')
    polys2,occurrence2 = Estimate_Poly_Over_All_Packets_Method_2(first_step_packets)
    print('\n\nPrinting the three most likely polynomials: \n')
    for i in range(len(polys2)):
        print('\nProbability to be the right polynomial is: ' + str(np.round(occurrence2[i],2)) + '%.')
        Print_All_Polynomial_Representations(polys2[i],crc_width)
    return first_step_packets,second_step_packets,crc_width
    
# %% Run main

if __name__ == '__main__':
    first_step_packets,second_step_packets,crc_width = Main()
    poly,crc_width,packet4,packet5 = Test_Packets_XorIn_Estimation()
    matrix = Run_Relative_Shift_Matrix(packet4,packet5,poly,crc_width)
    

# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:31:37 2022

@author: DanielT17
"""

# %% Imports

from .crc_utils import get_crc,print_crc_parameters
from .print_utils import print_packets
from crcengine import algorithms_available,new
from math import ceil
from .utils import bitstring_to_bytes
from logging import Logger
from typing import Any


# %% Functions

def print_start_program_text() -> None:
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

def choose_program_mode() -> int:
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

def create_example_mode_data(crc_algorithm: Any) -> list[bytes]:
    '''
    Description:
        This function holds the actual examples for example mode..
    Inputs:
        crc_algorithm - crcengine.calc._CrcLsbf - the crc object which will be
        used for the calculation.
    Outputs:
        packets - list - a list of packets with data + crc at the end.
        crc_width - int - the length of the crc polynomial.
    '''
    print('\nSimulated packet structure:')
    print('Preamble + Sync + Type + DST Address + SRC Address + Sequence Number + Data + CRC\n')
    preamble_header = bytearray([170,170])
    sync_header     = bytearray([154,125])
    type_header     = bytearray([0,1])
    dst_address     = bytearray([27,96])
    src_address     = bytearray([120,226])
    sequence_numbers = [bytearray([40,0]),bytearray([60,0]),bytearray([50,0]),bytearray([70,0]),bytearray([80,0]),bytearray([90,0]),bytearray([150,0]),bytearray([120,0]),bytearray([24,0]),bytearray([48,0]),bytearray([100,0]),bytearray([110,100,0]),bytearray([110,100,200,0]),bytearray([110,100,200,100,0])]
    data            = bytearray([5,10])
    packet_header = preamble_header + sync_header + type_header + dst_address + src_address
    packets: list[bytes] = []
    for sequence_number in sequence_numbers:
        packet = packet_header + sequence_number + data
        crc = get_crc(packet,crc_algorithm)
        packet = packet + crc
        packets.append(bytes(packet))
    print_packets(packets)
    return packets

def get_initial_example_mode_data() -> tuple[list[bytes], int]:
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
    print(list(algorithms_available()))
    while True:
        try:
            crc_algorithm_name = input('Write the name of the CRC code you want to reverse. \n\n')
            crc_algorithm = new(crc_algorithm_name)
            break
        except:
            print("\nPlese write the name of the algorithm correctly!\n\n")      
    crc_width = print_crc_parameters(crc_algorithm_name)
    packets = create_example_mode_data(crc_algorithm)
    return packets,crc_width

def check_data_input(packet: str, input_type: str, logger: Logger) -> bool:
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
            logger.critical("Critical path should not reach this.")
            raise RuntimeError("Critical path should not reach this.")
    return True
            

def get_initial_user_mode_data(logger: Logger) -> tuple[list[bytes], int]:
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
    crc_width = 0
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
    number_of_packets = 0
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
    data_type = ""
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
    print('Enter packets of equal length, optimal packets should have only one field changing, look at packets where only sequence number changes. \n')
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
                    if check_data_input(packet,data_type,logger):
                        if data_type == 'binary':
                            packets.append(bitstring_to_bytes(packet))
                        elif data_type == 'hex':
                            packets.append(bytes.fromhex(packet))
                        break
                    else:
                        print('Please enter the data in the following represesntation: ' + data_type + '.\n')
                except:
                    print('Please enter a packet with length bigger than one.')
    print_packets(packets)
    return packets,crc_width

def get_initial_data(program_mode: int, logger: Logger) -> tuple[list[bytes], int]:
    '''
    Description:
        This function gets the program_mode and creates a list of data+crc.
    Inputs:
        program_mode - int - choose program mode with respect to user input.
    Outputs:
        data_and_crcs - list - of combinations of data and crcs
    '''
    if program_mode == 1:
        packets,crc_width = get_initial_example_mode_data()
        
    elif program_mode == 2:
        packets,crc_width = get_initial_user_mode_data(logger)
    else:
        logger.critical("Critical path should not reach this.")
        raise RuntimeError("Critical path should not reach this.")
    return packets,crc_width

def start_program(logger: Logger) -> tuple[list[bytes], int]:
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
    print_start_program_text()
    program_mode = choose_program_mode()
    packets,crc_width = get_initial_data(program_mode,logger)
    return packets,crc_width

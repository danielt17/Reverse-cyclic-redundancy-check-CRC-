# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:38:13 2022

@author: DanielT17
"""

# %% Imports

from math import ceil
from typing import Tuple

# %% Functions

PacketPair = list[bytes]
PacketPairs = list[PacketPair]


def preprocessing(packets: list[bytes], crc_width: int) -> Tuple[PacketPairs, PacketPairs]:
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
    new_packets: PacketPairs = []
    for packet in packets:
        cur_packet = packet[:-crc_width//8];  cur_crc = packet[-crc_width//8:]
        packet_crc_pair: PacketPair = [cur_packet, cur_crc]
        new_packets.append(packet_crc_pair)
    num_packets = len(new_packets)
    first_step_packets_num = ceil(num_packets/1.5)
    if first_step_packets_num % 2 == 1:
        first_step_packets_num = first_step_packets_num - 1
    first_step_packets = new_packets[:first_step_packets_num]
    second_step_packets = new_packets[first_step_packets_num + 1:]
    return first_step_packets, second_step_packets


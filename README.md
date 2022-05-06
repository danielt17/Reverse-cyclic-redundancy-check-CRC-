# Reverse cyclic redundancy check (CRC) codes.

CRC reverse engneering is public tool to reverse engineer a CRC code parameters. The tool should be usefull for reverse engneering unknown communication protcols usually in link layer (Frames), especially for RF systems. In the figure below one can easily notice the existence of a CRC field, in case one does not know the CRC generator parameters, given some combinations of packet and CRC's he can recover the CRC generator parameters. This could be useful in case one wants to forge messages to look like valid messages.


<div align="center">

| ![Packet_Structure](https://user-images.githubusercontent.com/60748408/167182684-ff3d94b4-44ef-43c5-b20f-588950d53eb5.png ) |
|:---:|
| An example of a given packet structure, the CRC is present and could be unknown. |
</div>

## Agenda:

This program was written inorder to migrate CRC-REVENG to python, as being written in C makes it a lot harder to understand and to extended.


## README structure:

I will be going over the following topics:

1. Usage example (example mode and user mode).
2. Requirements.
3. A review of cylic redundancy check codes.
4. The algorithm.
5. Edge cases.

### Usage example:

This code has two modes of operation: 
1. Example mode where the user chooses a CRC from a list to reverse as an example.
2. User mode where the user enters his own packets (data+crc) to reverse the CRC for. 

Starting the program we are given the following options:

```
----------------------------------------

Cyclic redundancy check (CRC) reverse engneering tool.

----------------------------------------



There are two modes of running the tool: example mode, by choosing some known CRC with its full parameters, or user mode in which the user eneters his own packet with data and CRC values concatenated.

To enter example mode press 1, for user mode press 2.
```

#### Example mode:

Lets say we choose example mode by entering 1. we are now asked to choose out of a list of CRCs a CRC to reverse, the packets will be pregenerated.

```
You choose: example mode.

Choose one of the following choices and write its name below:

['crc8', 'crc8-autosar', 'crc8-bluetooth', 'crc8-ccitt', 'crc8-gsm-b', 'crc8-sae-j1850', 'crc15-can', 'crc16-kermit', 'crc16-ccitt-true', 'crc16-xmodem', 'crc16-autosar', 'crc16-ccitt-false', 'crc16-cdma2000', 'crc16-ibm', 'crc16-modbus', 'crc16-profibus', 'crc24-flexray16-a', 'crc24-flexray16-b', 'crc24-ble', 'crc24-interlaken', 'crc24-lte-a', 'crc24-lte-b', 'crc24-openpgp', 'crc24-os-9', 'crc32', 'crc32-flip-ref-in', 'crc32-flip-ref-out', 'crc32-bzip2', 'crc32-c', 'crc32-base91-d', 'crc32-cd-rom-edc', 'crc32-cksum', 'crc32-mef', 'crc32-xfer', 'crc40-gsm', 'crc64-ecma', 'crc64-go-iso', 'crc64-ms', 'crc64-we', 'crc64-xz']
Write the name of the CRC code you want to reverse.
```

Lets say we are going to choose: crc32, therefore at the start we will see the crc32 parameters which we want to reverse, and the simulated packets.

```
Cyclic redundancy check parameters:

poly: 0x4c11db7
width: 32.
seed: 4294967295.
ref_in: True.
ref_out: True.
xor_out: 4294967295.
name: crc32.



Simulated packet structure:
Preamble + Sync + Type + DST Address + SRC Address + Sequence Number + Data + CRC


Presenting packets inputed by user:

Packet 1: aaaa9a7d00011b6078e22800050a27d3bd69
Packet 2: aaaa9a7d00011b6078e23c00050af8a87da1
Packet 3: aaaa9a7d00011b6078e23200050a18770a92
Packet 4: aaaa9a7d00011b6078e24600050afc2a3d59
Packet 5: aaaa9a7d00011b6078e25000050a8958351a
Packet 6: aaaa9a7d00011b6078e25a00050ae6e5d57e
Packet 7: aaaa9a7d00011b6078e29600050ada7e84c0
Packet 8: aaaa9a7d00011b6078e27800050aecdeb2cb
Packet 9: aaaa9a7d00011b6078e21800050ad7f845c8
Packet 10: aaaa9a7d00011b6078e23000050ab27ec219
Packet 11: aaaa9a7d00011b6078e26400050af6115aec
Packet 12: aaaa9a7d00011b6078e26e6400050ae43a1f4b
Packet 13: aaaa9a7d00011b6078e26e64c800050ae197bc59
Packet 14: aaaa9a7d00011b6078e26e64c86400050a1596c60f
```

#### User mode:



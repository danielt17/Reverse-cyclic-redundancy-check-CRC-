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

From here the algorithm starts running in the same manner it would run for the usercase. A full output of the algorithm will be seen after I describe also the User mode.

#### User mode:

Lets say we choose user mode by entering 2. We are now asked to enter the polynomial degree, the algorithm assumes we know the degree of the CRC. In this example i choose to enter a polynomial degree of 40.

```
You choose: user mode.

Please write the CRC polynomial degree, a number between 8-128 including the limits:
```

The next parameter we are asked to input is the number of packets we are going to input into the algorithm, lets say 12.

```
Please enter the number of packets you want to enter, while the minimum number of packets is: 6 and the maximum is: 100 including the limits.
```

Afterwards we will be asked if the data we eneter is in binary or in hex the program can handle both, one just has to specify this here in advance.

```
Before entering your data please choose the representation you want to use: binary or hex. To choose binary write binary, to choose hexadecimal write hex.
```

Now we are asked to enter our packets in a concatanted form where packet = data + crc.

```
When enetering packets start with the data, and than concatenate the crc.

Enter packets of equal length, optimal packets should have only one field changing, look at packets where only sequence number changes.

Enter you packet in hexadecimal:
```

After inputting all of the packets, of equal and unequal length as requested by the program we will get the following:

```
When enetering packets start with the data, and than concatenate the crc.

Enter packets of equal length, optimal packets should have only one field changing, look at packets where only sequence number changes.

Enter you packet in hexadecimal: aaaa9a7d00011b6078e22800050a3dd91ac80b
Enter you packet in hexadecimal: aaaa9a7d00011b6078e23c00050a7869ca436a
Enter you packet in hexadecimal: aaaa9a7d00011b6078e23200050a9b97f38496
Enter you packet in hexadecimal: aaaa9a7d00011b6078e24600050ac55da33901
Enter you packet in hexadecimal: aaaa9a7d00011b6078e25000050aa07f7bf344
Enter you packet in hexadecimal: aaaa9a7d00011b6078e25a00050a02a552b6f0
Enter you packet in hexadecimal: aaaa9a7d00011b6078e29600050af73c635dc4
Enter you packet in hexadecimal: aaaa9a7d00011b6078e27800050a2b1edae586

Enter packets of unequal length

Enter you packet in hexadecimal: aaaa9a7d00011b6078e26400050aece62b6a77
Enter you packet in hexadecimal: aaaa9a7d00011b6078e26e6400050ad521480584
Enter you packet in hexadecimal: aaaa9a7d00011b6078e26e64c800050a24a8659b05
Enter you packet in hexadecimal: aaaa9a7d00011b6078e26e64c86400050a40db28c0be

Presenting packets inputed by user:

Packet 1: aaaa9a7d00011b6078e22800050a3dd91ac80b
Packet 2: aaaa9a7d00011b6078e23c00050a7869ca436a
Packet 3: aaaa9a7d00011b6078e23200050a9b97f38496
Packet 4: aaaa9a7d00011b6078e24600050ac55da33901
Packet 5: aaaa9a7d00011b6078e25000050aa07f7bf344
Packet 6: aaaa9a7d00011b6078e25a00050a02a552b6f0
Packet 7: aaaa9a7d00011b6078e29600050af73c635dc4
Packet 8: aaaa9a7d00011b6078e27800050a2b1edae586
Packet 9: aaaa9a7d00011b6078e26400050aece62b6a77
Packet 10: aaaa9a7d00011b6078e26e6400050ad521480584
Packet 11: aaaa9a7d00011b6078e26e64c800050a24a8659b05
Packet 12: aaaa9a7d00011b6078e26e64c86400050a40db28c0be
```

Reversing result:

```
-----------------------------------------------
Results of CRC reverse engneering algorithm:
-----------------------------------------------


-----------------------------------------------
poly:        0x4820009
width:       40
seed:        0x0
ref_in:      False
ref_out:     False
xor_out:     0xffffffffff
-----------------------------------------------
```

#### Full output

A full run of the algorithm would have the following structure:


```
----------------------------------------

Cyclic redundancy check (CRC) reverse engneering tool.

----------------------------------------



There are two modes of running the tool: example mode, by choosing some known CRC with its full parameters, or user mode in which the user eneters his own packet with data and CRC values concatenated.

To enter example mode press 1, for user mode press 2.
2

You choose: user mode.

Please write the CRC polynomial degree, a number between 8-128 including the limits:
40
Please enter the number of packets you want to enter, while the minimum number of packets is: 6 and the maximum is: 100 including the limits.
12
Before entering your data please choose the representation you want to use: binary or hex. To choose binary write binary, to choose hexadecimal write hex.
hex

Hexadecimal
When enetering packets start with the data, and than concatenate the crc.

Enter packets of equal length, optimal packets should have only one field changing, look at packets where only sequence number changes.

Enter you packet in hexadecimal: aaaa9a7d00011b6078e22800050a3dd91ac80b
Enter you packet in hexadecimal: aaaa9a7d00011b6078e23c00050a7869ca436a
Enter you packet in hexadecimal: aaaa9a7d00011b6078e23200050a9b97f38496
Enter you packet in hexadecimal: aaaa9a7d00011b6078e24600050ac55da33901
Enter you packet in hexadecimal: aaaa9a7d00011b6078e25000050aa07f7bf344
Enter you packet in hexadecimal: aaaa9a7d00011b6078e25a00050a02a552b6f0
Enter you packet in hexadecimal: aaaa9a7d00011b6078e29600050af73c635dc4
Enter you packet in hexadecimal: aaaa9a7d00011b6078e27800050a2b1edae586

Enter packets of unequal length

Enter you packet in hexadecimal: aaaa9a7d00011b6078e26400050aece62b6a77
Enter you packet in hexadecimal: aaaa9a7d00011b6078e26e6400050ad521480584
Enter you packet in hexadecimal: aaaa9a7d00011b6078e26e64c800050a24a8659b05
Enter you packet in hexadecimal: aaaa9a7d00011b6078e26e64c86400050a40db28c0be

Presenting packets inputed by user:

Packet 1: aaaa9a7d00011b6078e22800050a3dd91ac80b
Packet 2: aaaa9a7d00011b6078e23c00050a7869ca436a
Packet 3: aaaa9a7d00011b6078e23200050a9b97f38496
Packet 4: aaaa9a7d00011b6078e24600050ac55da33901
Packet 5: aaaa9a7d00011b6078e25000050aa07f7bf344
Packet 6: aaaa9a7d00011b6078e25a00050a02a552b6f0
Packet 7: aaaa9a7d00011b6078e29600050af73c635dc4
Packet 8: aaaa9a7d00011b6078e27800050a2b1edae586
Packet 9: aaaa9a7d00011b6078e26400050aece62b6a77
Packet 10: aaaa9a7d00011b6078e26e6400050ad521480584
Packet 11: aaaa9a7d00011b6078e26e64c800050a24a8659b05
Packet 12: aaaa9a7d00011b6078e26e64c86400050a40db28c0be



-------------------------------------------------
Estimating using method 1 (Xor-shift method):
-------------------------------------------------




Printing the three most likely polynomials:


Probability to be the right polynomial is: 33.33%.


----------------------------------------
Estimated CRC polynomial:
Normal mode:                     0x8d4fad1a98
Reverse mode:                    0x1958b5f2b1
Recipolar mode:                  0x32b16be563
Reversed recipolar mode:         0x1958b5f2b1
Recipolar reverse mode:          0x1a9f5a3531
Reversed recipolar reverse mode: 0xc6a7d68d4c
----------------------------------------


Probability to be the right polynomial is: 33.33%.


----------------------------------------
Estimated CRC polynomial:
Normal mode:                     0x8dbf011b7f
Reverse mode:                    0xfed880fdb1
Recipolar mode:                  0xfdb101fb63
Reversed recipolar mode:         0xfed880fdb1
Recipolar reverse mode:          0x1b7e0236ff
Reversed recipolar reverse mode: 0xc6df808dbf
----------------------------------------


Probability to be the right polynomial is: 33.33%.


----------------------------------------
Estimated CRC polynomial:
Normal mode:                     0x7c1238f827
Reverse mode:                    0xe41f1c483e
Recipolar mode:                  0xc83e38907d
Reversed recipolar mode:         0xe41f1c483e
Recipolar reverse mode:          0xf82471f04f
Reversed recipolar reverse mode: 0xbe091c7c13
----------------------------------------




--------------------------------------------
Estimating using method 2 (GCD method):
--------------------------------------------


The inputed packets don't supply enough information, please supply other packets.

The inputed packets don't supply enough information, please supply other packets.

The inputed packets don't supply enough information, please supply other packets.

The inputed packets don't supply enough information, please supply other packets.

The inputed packets don't supply enough information, please supply other packets.



Printing the three most likely polynomials:


Probability to be the right polynomial is: 80.0%.


----------------------------------------
Estimated CRC polynomial:
Normal mode:                     0x3618006c
Reverse mode:                    0x3600186c00
Recipolar mode:                  0x6c0030d801
Reversed recipolar mode:         0x3600186c00
Recipolar reverse mode:          0x6c3000d9
Reversed recipolar reverse mode: 0x801b0c0036
----------------------------------------


Probability to be the right polynomial is: 20.0%.


----------------------------------------
Estimated CRC polynomial:
Normal mode:                     0x4820009
Reverse mode:                    0x9000412000
Recipolar mode:                  0x2000824001
Reversed recipolar mode:         0x9000412000
Recipolar reverse mode:          0x9040013
Reversed recipolar reverse mode: 0x8002410004
----------------------------------------







-------------------------------------------------------------------------------------
The list of polynomials we will continue to use in our XorIn estimation procedure:
-------------------------------------------------------------------------------------



Probability to be the right polynomial is: 40.0%.


----------------------------------------
Estimated CRC polynomial:
Normal mode:                     0x8d4fad1a98
Reverse mode:                    0x1958b5f2b1
Recipolar mode:                  0x32b16be563
Reversed recipolar mode:         0x1958b5f2b1
Recipolar reverse mode:          0x1a9f5a3531
Reversed recipolar reverse mode: 0xc6a7d68d4c
----------------------------------------


Probability to be the right polynomial is: 16.67%.


----------------------------------------
Estimated CRC polynomial:
Normal mode:                     0x7c1238f827
Reverse mode:                    0xe41f1c483e
Recipolar mode:                  0xc83e38907d
Reversed recipolar mode:         0xe41f1c483e
Recipolar reverse mode:          0xf82471f04f
Reversed recipolar reverse mode: 0xbe091c7c13
----------------------------------------


Probability to be the right polynomial is: 16.67%.


----------------------------------------
Estimated CRC polynomial:
Normal mode:                     0x3618006c
Reverse mode:                    0x3600186c00
Recipolar mode:                  0x6c0030d801
Reversed recipolar mode:         0x3600186c00
Recipolar reverse mode:          0x6c3000d9
Reversed recipolar reverse mode: 0x801b0c0036
----------------------------------------


Probability to be the right polynomial is: 16.67%.


----------------------------------------
Estimated CRC polynomial:
Normal mode:                     0x4820009
Reverse mode:                    0x9000412000
Recipolar mode:                  0x2000824001
Reversed recipolar mode:         0x9000412000
Recipolar reverse mode:          0x9040013
Reversed recipolar reverse mode: 0x8002410004
----------------------------------------


Probability to be the right polynomial is: 10.0%.


----------------------------------------
Estimated CRC polynomial:
Normal mode:                     0x8dbf011b7f
Reverse mode:                    0xfed880fdb1
Recipolar mode:                  0xfdb101fb63
Reversed recipolar mode:         0xfed880fdb1
Recipolar reverse mode:          0x1b7e0236ff
Reversed recipolar reverse mode: 0xc6df808dbf
----------------------------------------







------------------------------------------------------------------------------------------------
Estimated XorIn (seed) values and its relevant generator polynomial, and actual polynomial:
------------------------------------------------------------------------------------------------



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x8d4fad1a98
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x8d4fad1a99
Estimated XorIn (seed):      0xf61dc08d7c', '0x6f45757fcd', '0x2d5d04a404', '0xb405b156b5', '0x91eb6aa4ba', '0x8b3df560b', '0xffffffffff', '0x0', '0xb69ebfe5f2', '0x2fc60a1743', '0x122b03d4f2', '0x8b73b62643', '0x25233651e0', '0xbc7b83a351



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x18d4fad1a98
Estimated XorIn (seed):      0x4d755cc8d8', '0xd0634f72f1', '0xe2d2249792', '0x7fc4372dbb', '0x87b0f35d54', '0x1aa6e0e77d', '0x28178b021e', '0xb50198b837', '0xaa6fecf630', '0x3779ff4c19', '0x5c894a97a', '0x98de871353', '0x60aa4363bc', '0xfdbc50d995', '0xcf0d3b3cf6', '0x521b2886df', '0xca832cecd0', '0x57953f56f9', '0x652454b39a', '0xf8324709b3', '0x4683795c', '0x9d5090c375', '0xafe1fb2616', '0x32f7e89c3f', '0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x1958b5f2b1
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x1958b5f2b2
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x11958b5f2b1
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x32b16be563
Estimated XorIn (seed):      0x1ef6b93e0', '0x95b2a3fb59', '0xa41b56580a', '0x30469e30b3', '0xc748bd1eac', '0x5315757615', '0x62bc80d546', '0xf6e148bdff', '0x9b2f810', '0x94547a90a9', '0xa5fd8f33fa', '0x31a0475b43', '0xc6ae64755c', '0x52f3ac1de5', '0x635a59beb6', '0xf70791d60f', '0x6b9f741288', '0xffc2bc7a31', '0xce6b49d962', '0x5a3681b1db', '0xad38a29fc4', '0x39656af77d', '0x8cc9f542e', '0x9c91573c97', '0xffffffffff', '0x0', '0x60b066f298', '0xf4edae9a21', '0xc5445b3972', '0x51199351cb', '0xa617b07fd4', '0x324a78176d', '0x3e38db43e', '0x97be45dc87', '0x2ac1d0d528', '0xbe9c18bd91', '0x8f35ed1ec2', '0x1b6825767b', '0xec66065864', '0x783bce30dd', '0x49923b938e', '0xddcff3fb37', '0x7593c339a8', '0xe1ce0b5111', '0xd067fef242', '0x443a369afb', '0xb33415b4e4', '0x2769dddc5d', '0x16c0287f0e', '0x829de017b7



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x32b16be564
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x132b16be563
Estimated XorIn (seed):      0x8ca0e31b5a', '0x86587ed2d', '0x58b64c58c4', '0xdc7328aeb3', '0x62768f9d78', '0xe6b3eb6b0f', '0xffffffffff', '0x0', '0xd37b1d08a4', '0x57be79fed3', '0x24bae413c8', '0xa07f80e5bf', '0xeb60d16068', '0x6fa5b5961f



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x1958b5f2b1
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x1958b5f2b2
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x11958b5f2b1
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x1a9f5a3531
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x1a9f5a3532
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x11a9f5a3531
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0xc6a7d68d4c
Estimated XorIn (seed):      0x4d755cc8d8', '0xd0634f72f1', '0xe2d2249792', '0x7fc4372dbb', '0x87b0f35d54', '0x1aa6e0e77d', '0x28178b021e', '0xb50198b837', '0xaa6fecf630', '0x3779ff4c19', '0x5c894a97a', '0x98de871353', '0x60aa4363bc', '0xfdbc50d995', '0xcf0d3b3cf6', '0x521b2886df', '0xca832cecd0', '0x57953f56f9', '0x652454b39a', '0xf8324709b3', '0x4683795c', '0x9d5090c375', '0xafe1fb2616', '0x32f7e89c3f', '0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0xc6a7d68d4d
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8d4fad1a98
Actual polynomial:           0x1c6a7d68d4c
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0x7c1238f827
Estimated XorIn (seed):      0xd65e722928', '0x404ee04509', '0x32416e6116', '0xa451fc0d37', '0x9f80cd8c88', '0x9905fe0a9', '0x7b9fd1c4b6', '0xed8f43a897', '0x1134178c8c', '0x872485e0ad', '0xf52b0bc4b2', '0x633b99a893', '0xffffffffff', '0x0', '0x69432cb43c', '0xff53bed81d', '0x8d5c30fc02', '0x1b4ca29023', '0x402048633c', '0xd630da0f1d', '0xa43f542b02', '0x322fc64723', '0xbed3895818', '0x28c31b3439', '0x5acc951026', '0xccdc077c07



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0x7c1238f828
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0x17c1238f827
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0xe41f1c483e
Estimated XorIn (seed):      0xc5500c34b8', '0x4166453cd1', '0x3d747dc4f6', '0xb94234cc9f', '0xba81611828', '0x3eb7281041', '0x42a510e866', '0xc69359e00f', '0x9945726e10', '0x1d733b6679', '0x6161039e5e', '0xe5574a9637', '0xffffffffff', '0x0', '0x263ff368d0', '0xa209ba60b9', '0xde1b82989e', '0x5a2dcb90f7



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0xe41f1c483f
Estimated XorIn (seed):      0xa01de77178', '0xf413f0d965', '0x801c82142', '0x5c0fdf895f', '0xe49090c958', '0xb09e876145', '0x4c8cbf9962', '0x1882a8317f', '0x24941072c8', '0x709a07dad5', '0x8c883f22f2', '0xd886288aef', '0xffffffffff', '0x0', '0xbc2f402360', '0xe821578b7d', '0x14336f735a', '0x403d78db47', '0xe08c49bee4', '0xb4825e16f9', '0x489066eede', '0x1c9e7146c3', '0x6c203464ac', '0x382e23ccb1', '0xc43c1b3496', '0x90320c9c8b



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0x1e41f1c483e
Estimated XorIn (seed):      0xbcea416be0', '0xeb0991c425', '0x132de0346a', '0x44ce309baf', '0xc830832768', '0x9fd35388ad', '0x67f72278e2', '0x3014f2d727', '0x43aea70e60', '0x144d77a1a5', '0xec690651ea', '0xbb8ad6fe2f', '0xffffffffff', '0x0', '0x8f95e52bb0', '0xd876358475', '0x205244743a', '0x77b194dbff



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0xc83e38907d
Estimated XorIn (seed):      0xb9ab03f294', '0x7a21f8e87', '0x2edfd1695a', '0x90d6cd1549', '0xa528835868', '0x1b219f247b', '0xffffffffff', '0x0', '0x293d586346', '0x9734441f55', '0x6e90158da2', '0xd09909f1b1', '0x6abb563bcc', '0xd4b24a47df



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0xc83e38907e
Estimated XorIn (seed):      0xeb72f0ca38', '0x6969d44e0d', '0x1760c8321e', '0x957becb62b', '0xf159af9a78', '0x73428b1e4d', '0xd4b97625e', '0x8f50b3e66b', '0xb0bcb50f5c', '0x32a7918b69', '0x4cae8df77a', '0xceb5a9734f', '0xffffffffff', '0x0', '0xaeae24fc10', '0x2cb5007825', '0x52bc1c0436', '0xd0a7388003



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0x1c83e38907d
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0xe41f1c483e
Estimated XorIn (seed):      0xc5500c34b8', '0x4166453cd1', '0x3d747dc4f6', '0xb94234cc9f', '0xba81611828', '0x3eb7281041', '0x42a510e866', '0xc69359e00f', '0x9945726e10', '0x1d733b6679', '0x6161039e5e', '0xe5574a9637', '0xffffffffff', '0x0', '0x263ff368d0', '0xa209ba60b9', '0xde1b82989e', '0x5a2dcb90f7



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0xe41f1c483f
Estimated XorIn (seed):      0xa01de77178', '0xf413f0d965', '0x801c82142', '0x5c0fdf895f', '0xe49090c958', '0xb09e876145', '0x4c8cbf9962', '0x1882a8317f', '0x24941072c8', '0x709a07dad5', '0x8c883f22f2', '0xd886288aef', '0xffffffffff', '0x0', '0xbc2f402360', '0xe821578b7d', '0x14336f735a', '0x403d78db47', '0xe08c49bee4', '0xb4825e16f9', '0x489066eede', '0x1c9e7146c3', '0x6c203464ac', '0x382e23ccb1', '0xc43c1b3496', '0x90320c9c8b



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0x1e41f1c483e
Estimated XorIn (seed):      0xbcea416be0', '0xeb0991c425', '0x132de0346a', '0x44ce309baf', '0xc830832768', '0x9fd35388ad', '0x67f72278e2', '0x3014f2d727', '0x43aea70e60', '0x144d77a1a5', '0xec690651ea', '0xbb8ad6fe2f', '0xffffffffff', '0x0', '0x8f95e52bb0', '0xd876358475', '0x205244743a', '0x77b194dbff



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0xf82471f04f
Estimated XorIn (seed):      0xc41ff5abc', '0x5dbb7ab949', '0xafb4f49d56', '0xfe4e717ea3', '0x8fa9271fb8', '0xde53a2fc4d', '0x2c5c2cd852', '0x7da6a93ba7', '0xdfbcc76a30', '0x8e464289c5', '0x7c49ccadda', '0x2db3494e2f', '0xffffffffff', '0x0', '0xaea7f10ef0', '0xff5d74ed05', '0xd52fac91a', '0x5ca87f2aef', '0x8ef0403320', '0xdf0ac5d0d5', '0x2d054bf4ca', '0x7cffce173f', '0x94871f78a8', '0xc57d9a9b5d', '0x377214bf42', '0x6688915cb7



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0xf82471f050
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0x1f82471f04f
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0xbe091c7c13
Estimated XorIn (seed):      0x72c716afdc', '0xbaf92e3fa1', '0x1b15e206bc', '0xd32bda96c1', '0xc562fb7f16', '0xd5cc3ef6b', '0xffffffffff', '0x0', '0xb43d6ee0b8', '0x7c035670c5', '0x2cb53bce72', '0xe48b035e0f', '0xcbbb2ddb5a', '0x385154b27



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0xbe091c7c14
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x7c1238f827
Actual polynomial:           0x1be091c7c13
Estimated XorIn (seed):      0x46bd0f173c', '0xc969200895', '0xa72028f668', '0x28f407e9c1', '0x3326d3b19c', '0xbcf2fcae35', '0xffffffffff', '0x0', '0x52e0fc5836', '0xdd34d3479f', '0x8018d558b8', '0xfccfa4711', '0x6136b5e57e', '0xeee29afad7



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x3618006c
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x3618006d
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x1003618006c
Estimated XorIn (seed):      0xe08724b430', '0x8c87146c31', '0x3887450432', '0x548775dc33', '0xc21e7ff684', '0xae1e4f2e85', '0x1a1e1e4686', '0x761e2e9e87', '0xb5639e268', '0x6756093a69', '0xd35658526a', '0xbf56688a6b', '0xffffffffff', '0x0



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x3600186c00
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x3600186c01
Estimated XorIn (seed):      0x59a8892c10', '0xb9881b2c51', '0x99859d2c4a', '0x79a50f2c0b', '0xd99e912c7c', '0x39be032c3d', '0x19b3852c26', '0xf993172c67', '0x39cc25f718', '0xd9ecb7f759', '0xf9e131f742', '0x19c1a3f703', '0xb9fa3df774', '0x59daaff735', '0x79d729f72e', '0x99f7bbf76f', '0x4beafed218', '0xabca6cd259', '0x8bc7ead242', '0x6be778d203', '0xcbdce6d274', '0x2bfc74d235', '0xbf1f2d22e', '0xebd160d26f', '0xffffffffff', '0x0', '0xb054442880', '0x5074d628c1', '0x70795028da', '0x9059c2289b', '0x30625c28ec', '0xd042ce28ad', '0xf04f4828b6', '0x106fda28f7', '0xeddd9421a8', '0xdfd0621e9', '0x2df08021f2', '0xcdd01221b3', '0x6deb8c21c4', '0x8dcb1e2185', '0xadc698219e', '0x4de60a21df', '0x7b7fed3750', '0x9b5f7f3711', '0xbb52f9370a', '0x5b726b374b', '0xfb49f5373c', '0x1b6967377d', '0x3b64e13766', '0xdb44733727



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x13600186c00
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x3600186c
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x6c0030d801
Estimated XorIn (seed):      0x710720dcc4', '0xb111aadce9', '0xf11c2cdcf2', '0x310aa6dcdf', '0xd727589f3c', '0x1731d29f11', '0x573c549f0a', '0x972ade9f27', '0xea244b5dd4', '0x2a32c15df9', '0x6a3f475de2', '0xaa29cd5dcf', '0xffffffffff', '0x0', '0x3ccb805e4c', '0xfcdd0a5e61', '0xbcd08c5e7a', '0x7cc6065e57', '0xdfb4da56f8', '0x1fa25056d5', '0x5fafd656ce', '0x9fb95c56e3', '0xb0fdfac2cc', '0x70eb70c2e1', '0x30e6f6c2fa', '0xf0f07cc2d7



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x6c0030d802
Estimated XorIn (seed):      0x59a8892c10', '0xb9881b2c51', '0x99859d2c4a', '0x79a50f2c0b', '0xd99e912c7c', '0x39be032c3d', '0x19b3852c26', '0xf993172c67', '0x39cc25f718', '0xd9ecb7f759', '0xf9e131f742', '0x19c1a3f703', '0xb9fa3df774', '0x59daaff735', '0x79d729f72e', '0x99f7bbf76f', '0x4beafed218', '0xabca6cd259', '0x8bc7ead242', '0x6be778d203', '0xcbdce6d274', '0x2bfc74d235', '0xbf1f2d22e', '0xebd160d26f', '0xffffffffff', '0x0', '0xeddd9421a8', '0xdfd0621e9', '0x2df08021f2', '0xcdd01221b3', '0x6deb8c21c4', '0x8dcb1e2185', '0xadc698219e', '0x4de60a21df



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x16c0030d801
Estimated XorIn (seed):      0x1b67ca65be', '0xe48a3d9a65', '0x3121d3823a', '0xcecc247de1', '0x7027c40828', '0x8fca33f7f3', '0xffffffffff', '0x0', '0xfc33eda05e', '0x3de1a5f85', '0x948911e050', '0x6b64e61f8b', '0x248091fbd8', '0xdb6d660403



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x3600186c00
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x3600186c01
Estimated XorIn (seed):      0x59a8892c10', '0xb9881b2c51', '0x99859d2c4a', '0x79a50f2c0b', '0xd99e912c7c', '0x39be032c3d', '0x19b3852c26', '0xf993172c67', '0x39cc25f718', '0xd9ecb7f759', '0xf9e131f742', '0x19c1a3f703', '0xb9fa3df774', '0x59daaff735', '0x79d729f72e', '0x99f7bbf76f', '0x4beafed218', '0xabca6cd259', '0x8bc7ead242', '0x6be778d203', '0xcbdce6d274', '0x2bfc74d235', '0xbf1f2d22e', '0xebd160d26f', '0xffffffffff', '0x0', '0xb054442880', '0x5074d628c1', '0x70795028da', '0x9059c2289b', '0x30625c28ec', '0xd042ce28ad', '0xf04f4828b6', '0x106fda28f7', '0xeddd9421a8', '0xdfd0621e9', '0x2df08021f2', '0xcdd01221b3', '0x6deb8c21c4', '0x8dcb1e2185', '0xadc698219e', '0x4de60a21df', '0x7b7fed3750', '0x9b5f7f3711', '0xbb52f9370a', '0x5b726b374b', '0xfb49f5373c', '0x1b6967377d', '0x3b64e13766', '0xdb44733727



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x13600186c00
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x3600186c
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x6c3000d9
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x6c3000da
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x1006c3000d9
Estimated XorIn (seed):      0x5b601dc4d4', '0xb69fea1f2b', '0xa8c2a4d498', '0x453d530f67', '0xfd8d4b7784', '0x1072bcac7b', '0xffffffffff', '0x0', '0x5929862c42', '0xb4d671f7bd', '0x53155d7cba', '0xbeeaaaa745', '0x6831118b4e', '0x85cee650b1



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x801b0c0036
Estimated XorIn (seed):      0xe08724b430', '0x8c87146c31', '0x3887450432', '0x548775dc33', '0xc21e7ff684', '0xae1e4f2e85', '0x1a1e1e4686', '0x761e2e9e87', '0xb5639e268', '0x6756093a69', '0xd35658526a', '0xbf56688a6b', '0xffffffffff', '0x0', '0x9fcd4c5a84', '0xf3cd7c8285', '0x47cd2dea86', '0x2bcd1d3287



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x801b0c0037
Estimated XorIn (seed):      0x86301ea248', '0x6a302e7a49', '0xeb655478e2', '0x76564a0e3', '0x5c9a8b171c', '0xb09abbcf1d', '0x31cfc1cdb6', '0xddcff115b7', '0xffffffffff', '0x0', '0xcc84a4e2b8', '0x2084943ab9', '0xa1d1ee3812', '0x4dd1dee013', '0x162e3157ec', '0xfa2e018fed', '0x7b7b7b8d46', '0x977b4b5547



Generator polynomial (taps): 0x3618006c
Actual polynomial:           0x1801b0c0036
Estimated XorIn (seed):      0xefd8414900', '0xa7d861d901', '0x7fd8006902', '0x37d820f903', '0xfd83f76fc', '0x47d81fe6fd', '0x9fd87e56fe', '0xd7d85ec6ff', '0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x4820009
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x482000a
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x10004820009
Estimated XorIn (seed):      0x6e39bfed7e', '0x8e39c1d281', '0x970c47e518', '0x770c39dae7', '0xe28742fc02', '0x2873cc3fd', '0xffffffffff', '0x0', '0xe0007e3fff



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x9000412000
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x9000412001
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x19000412000
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x9000412
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x2000824001
Estimated XorIn (seed):      0x3177038f88', '0x117793cf89', '0x7176230f8a', '0x5176b34f8b', '0xb175428f8c', '0x9175d2cf8d', '0xf174620f8e', '0xd174f24f8f', '0x70325d37c8', '0x5032cd77c9', '0x30337db7ca', '0x1033edf7cb', '0xf0301c37cc', '0xd0308c77cd', '0xb0313cb7ce', '0x9031acf7cf', '0x3448e775c0', '0x14487735c1', '0x7449c7f5c2', '0x544957b5c3', '0xb44aa675c4', '0x944a3635c5', '0xf44b86f5c6', '0xd44b16b5c7', '0xffffffffff', '0x0', '0x6910c91500', '0x4910595501', '0x2911e99502', '0x91179d503', '0xe912881504', '0xc912185505', '0xa913a89506', '0x891338d507', '0x2cdb128f58', '0xcdb82cf59', '0x6cda320f5a', '0x4cdaa24f5b', '0xacd9538f5c', '0x8cd9c3cf5d', '0xecd8730f5e', '0xccd8e34f5f', '0xe63682d570', '0xc636129571', '0xa637a25572', '0x8637321573', '0x6634c3d574', '0x4634539575', '0x2635e35576', '0x635731577



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x2000824002
Estimated XorIn (seed):      0xd79b82ca90', '0xc79b128a91', '0xf79aa24a92', '0xe79a320a93', '0x9799c3ca94', '0x8799538a95', '0xb798e34a96', '0xa798730a97', '0x579f00ca98', '0x479f908a99', '0x779e204a9a', '0x679eb00a9b', '0x179d41ca9c', '0x79dd18a9d', '0x379c614a9e', '0x279cf10a9f', '0x9a1c590660', '0x8a1cc94661', '0xba1d798662', '0xaa1de9c663', '0xda1e180664', '0xca1e884665', '0xfa1f388666', '0xea1fa8c667', '0x1a18db0668', '0xa184b4669', '0x3a19fb866a', '0x2a196bc66b', '0x5a1a9a066c', '0x4a1a0a466d', '0x7a1bba866e', '0x6a1b2ac66f', '0x1fe3a1f2b0', '0xfe331b2b1', '0x3fe28172b2', '0x2fe21132b3', '0x5fe1e0f2b4', '0x4fe170b2b5', '0x7fe0c072b6', '0x6fe05032b7', '0x9fe723f2b8', '0x8fe7b3b2b9', '0xbfe60372ba', '0xafe69332bb', '0xdfe562f2bc', '0xcfe5f2b2bd', '0xffe44272be', '0xefe4d232bf', '0xffffffffff', '0x0', '0x7f2010ef10', '0x6f2080af11', '0x5f21306f12', '0x4f21a02f13', '0x3f2251ef14', '0x2f22c1af15', '0x1f23716f16', '0xf23e12f17', '0xff2492ef18', '0xef2402af19', '0xdf25b26f1a', '0xcf25222f1b', '0xbf26d3ef1c', '0xaf2643af1d', '0x9f27f36f1e', '0x8f27632f1f



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x12000824001
Estimated XorIn (seed):      0xe82d411ea8', '0x17d13f1eaf', '0x396846b9d0', '0xc69438b9d7', '0x80bebdc78e', '0x7f42c3c789', '0xffffffffff', '0x0', '0xe09901c132', '0x1f657fc135', '0xef4b01de96', '0x10b77fde91', '0xc28cfe7ae6', '0x3d70807ae1



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x9000412000
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x9000412001
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x19000412000
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x9000412
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x9040013
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x9040014
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x10009040013
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x8002410004
Estimated XorIn (seed):      0xba8d02c480', '0x9a8d808481', '0xfa8c064482', '0xda8c840483', '0x3a8f0bc484', '0x1a8f898485', '0x7a8e0f4486', '0x5a8e8d0487', '0x179327d080', '0x3793a59081', '0x5792235082', '0x7792a11083', '0x97912ed084', '0xb791ac9085', '0xd7902a5086', '0xf790a81087', '0xb09b9d5e8', '0x2b093b95e9', '0x4b08bd55ea', '0x6b083f15eb', '0x8b0bb0d5ec', '0xab0b3295ed', '0xcb0ab455ee', '0xeb0a3615ef', '0xffffffffff', '0x0



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x8002410005
Estimated XorIn (seed):      0xc682488fc0', '0x6682cacfc1', '0x86821ca56a', '0x26829ee56b', '0x4682e0da94', '0xe682629a95', '0x682b4f03e', '0xa68236b03f', '0xffffffffff', '0x0', '0x2f6329b548', '0x8f63abf549', '0x6f637d9fe2', '0xcf63ffdfe3', '0xaf6381e01c', '0xf6303a01d', '0xef63d5cab6', '0x4f63578ab7



Generator polynomial (taps): 0x4820009
Actual polynomial:           0x18002410004
Estimated XorIn (seed):      0xe553e9ea50', '0xdaacea6a51', '0x9aadeeea52', '0xa552ed6a53', '0x1aafe7ea54', '0x2550e46a55', '0x6551e0ea56', '0x5aaee36a57', '0x4ffbe215a8', '0x7004e195a9', '0x3005e515aa', '0xffae695ab', '0xb007ec15ac', '0x8ff8ef95ad', '0xcff9eb15ae', '0xf006e895af', '0xffffffffff', '0x0



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0x8dbf011b7f
Estimated XorIn (seed):      0x5b743a1718', '0xa5acbaeaa9', '0x966d448570', '0x68b5c478c1', '0xf759181de4', '0x98198e055', '0xffffffffff', '0x0', '0x48ee5c885c', '0xb636dc75ed', '0x9f9387a5a', '0xf721b887eb', '0x394c8a33f8', '0xc7940ace49



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0x8dbf011b80
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0x18dbf011b7f
Estimated XorIn (seed):      0x3faa081b1c', '0x94c508b23d', '0xbeb335109e', '0x15dc35b9bf', '0x134ebdfbde', '0xb821bd52ff', '0xffffffffff', '0x0', '0x6ad77e0dc8', '0xc1b87ea4e9', '0xb02d50d33a', '0x1b42507a1b', '0xf2155751a0', '0x597a57f881



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0xfed880fdb1
Estimated XorIn (seed):      0x306704af48', '0xbdd805b437', '0x357597fb22', '0xb8ca96e05d', '0x5160c97c24', '0xdcdfc8675b', '0xffffffffff', '0x0', '0x20fda2fa52', '0xad42a3e12d', '0x46da899942', '0xcb6588823d', '0xfc3327b200', '0x718c26a97f



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0xfed880fdb2
Estimated XorIn (seed):      0xd855b6c9b4', '0xe94b5e435', '0x432bb4ff4a', '0x95eab7d2cb', '0xa8f7022c70', '0x7e360101f1', '0x3389001a8e', '0xe54803370f', '0x841e10f52c', '0x52df13d8ad', '0x1f6012c3d2', '0xc9a111ee53', '0xffffffffff', '0x0', '0xc11c71c8a4', '0x17dd72e525', '0x5a6273fe5a', '0x8ca370d3db



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0x1fed880fdb1
Estimated XorIn (seed):      0xb914fc7c', '0xf66ceaee29', '0xa42040e01a', '0x52f5bef24f', '0xffffffffff', '0x0', '0xd83d861578', '0x2ee878072d', '0x7ca4d2091e', '0x8a712c1b4b



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0xfdb101fb63
Estimated XorIn (seed):      0xb821244878', '0x7efea4c5c7', '0x23bf3738ee', '0xe560b7b551', '0xcc8aa54ca2', '0xa5525c11d', '0xffffffffff', '0x0', '0xc27ab29e74', '0x4a53213cb', '0x686e5692b6', '0xaeb1d61f09', '0xba4c9bdd3a', '0x7c931b5085



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0xfdb101fb64
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0x1fdb101fb63
Estimated XorIn (seed):      0x124d93f1cc', '0x96d8930719', '0xca0e35a596', '0x4e9b355343', '0xbb24f99a1a', '0x3fb1f96ccf', '0xffffffffff', '0x0', '0xb32ba97160', '0x37bea987b5', '0x4343ca35cc', '0xc7d6cac319', '0x7c9625c9fa', '0xf803253f2f



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0xfed880fdb1
Estimated XorIn (seed):      0x306704af48', '0xbdd805b437', '0x357597fb22', '0xb8ca96e05d', '0x5160c97c24', '0xdcdfc8675b', '0xffffffffff', '0x0', '0x20fda2fa52', '0xad42a3e12d', '0x46da899942', '0xcb6588823d', '0xfc3327b200', '0x718c26a97f



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0xfed880fdb2
Estimated XorIn (seed):      0xd855b6c9b4', '0xe94b5e435', '0x432bb4ff4a', '0x95eab7d2cb', '0xa8f7022c70', '0x7e360101f1', '0x3389001a8e', '0xe54803370f', '0x841e10f52c', '0x52df13d8ad', '0x1f6012c3d2', '0xc9a111ee53', '0xffffffffff', '0x0', '0xc11c71c8a4', '0x17dd72e525', '0x5a6273fe5a', '0x8ca370d3db



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0x1fed880fdb1
Estimated XorIn (seed):      0xb914fc7c', '0xf66ceaee29', '0xa42040e01a', '0x52f5bef24f', '0xffffffffff', '0x0', '0xd83d861578', '0x2ee878072d', '0x7ca4d2091e', '0x8a712c1b4b



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0x1b7e0236ff
Estimated XorIn (seed):      0xe758c46b60', '0xb8d87c4461', '0x5859b43562', '0x7d90c1a63', '0x6782a42ad4', '0x38021c05d5', '0xd883d474d6', '0x87036c5bd7', '0x18348415b8', '0x47b43c3ab9', '0xa735f44bba', '0xf8b54c64bb', '0x98eee4540c', '0xc76e5c7b0d', '0x27ef940a0e', '0x786f2c250f', '0x5f725deb00', '0xf2e5c401', '0xe0732db502', '0xbff3959a03', '0xdfa83daab4', '0x80288585b5', '0x60a94df4b6', '0x3f29f5dbb7', '0xa01e1d95d8', '0xff9ea5bad9', '0x1f1f6dcbda', '0x409fd5e4db', '0x20c47dd46c', '0x7f44c5fb6d', '0x9fc50d8a6e', '0xc045b5a56f', '0x8ff9807fc0', '0xd0793850c1', '0x30f8f021c2', '0x6f78480ec3', '0xf23e03e74', '0x50a3581175', '0xb022906076', '0xefa2284f77', '0x7095c00118', '0x2f15782e19', '0xcf94b05f1a', '0x901408701b', '0xf04fa040ac', '0xafcf186fad', '0x4f4ed01eae', '0x10ce6831af', '0xffffffffff', '0x0', '0x7fccd7f440', '0x204c6fdb41', '0xc0cda7aa42', '0x9f4d1f8543', '0xff16b7b5f4', '0xa0960f9af5', '0x4017c7ebf6', '0x1f977fc4f7', '0x80a0978a98', '0xdf202fa599', '0x3fa1e7d49a', '0x60215ffb9b', '0x7af7cb2c', '0x5ffa4fe42d', '0xbf7b87952e', '0xe0fb3fba2f', '0xd1164da2f0', '0x8e96f58df1', '0x6e173dfcf2', '0x319785d3f3', '0x51cc2de344', '0xe4c95cc45', '0xeecd5dbd46', '0xb14de59247', '0x2e7a0ddc28', '0x71fab5f329', '0x917b7d822a', '0xcefbc5ad2b', '0xaea06d9d9c', '0xf120d5b29d', '0x11a11dc39e', '0x4e21a5ec9f', '0xef68cddbc0', '0xb0e875f4c1', '0x5069bd85c2', '0xfe905aac3', '0x6fb2ad9a74', '0x303215b575', '0xd0b3ddc476', '0x8f3365eb77', '0x10048da518', '0x4f84358a19', '0xaf05fdfb1a', '0xf08545d41b', '0x90deede4ac', '0xcf5e55cbad', '0x2fdf9dbaae', '0x705f2595af



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0x1b7e023700
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0x11b7e0236ff
Estimated XorIn (seed):      0xf62ce4c610', '0x9014ce5f35', '0x3a5cb1f45a', '0x5c649b6d7f', '0xffffffffff', '0x0', '0x479144065c', '0x21a96e9f79', '0x8be1113416', '0xedd93bad33



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0xc6df808dbf
Estimated XorIn (seed):      0x70c6f5d610', '0x8d77f42d73', '0xed0b69ab18', '0x10ba68507b', '0x4542eeb3e', '0xf9e52f105d', '0xffffffffff', '0x0', '0x1893361f36', '0xe52237e455', '0xe7c4e7b21c', '0x1a75e6497f', '0xcb2b5e056', '0xf103b41b35



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0xc6df808dc0
Estimated XorIn (seed):      0xffffffffff', '0x0



Generator polynomial (taps): 0x8dbf011b7f
Actual polynomial:           0x1c6df808dbf
Estimated XorIn (seed):      0xffffffffff', '0x0



-----------------------------------------------







----------------------------------
Estimated XorOut combinations:
----------------------------------



Generator polynomial (taps): 0x4820009
Estimated XorIn (seed):      0x0
Estimated XorOut (Mask/Final):     0xffffffffff


















-----------------------------------------------
Results of CRC reverse engneering algorithm:
-----------------------------------------------


-----------------------------------------------
poly:        0x4820009
width:       40
seed:        0x0
ref_in:      False
ref_out:     False
xor_out:     0xffffffffff
-----------------------------------------------


```





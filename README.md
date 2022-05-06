# Reverse cyclic redundancy check (CRC)

CRC reverse engneering is public tool to reverse engineer a CRC code parameters. The tool should be usefull for reverse engneering unknown communication protcols usually in link layer (Frames), especially for RF systems. In the figure below one can easily notice the existence of a CRC field, in case one does not know the CRC generator parameters, given some combinations of packet and CRC's he can recover the CRC generator parameters. This could be useful in case one wants to forge messages to look like valid messages.


<div align="center">

| ![Packet_Structure](https://user-images.githubusercontent.com/60748408/167182684-ff3d94b4-44ef-43c5-b20f-588950d53eb5.png ) |
|:---:|
| An example of a given packet structure, the CRC is present and could be unknown. |
</div>






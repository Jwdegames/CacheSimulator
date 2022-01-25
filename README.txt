This project implements a cache simulator with a cache of 8 address bits. To run the program execute python cachesimulator.py <filename>

<filename> should be the name of the RAM contents. This file should have 1 hexadecimal byte in uppercase on each line.

When the program starts, you will be asked to initialize the RAM. Enter init-ram <start address> <end address>

<start address> and <end address> are hexadecimal values in the form of 0x## where # is a hexadecimal digit in upper case.

The RAM is limited to a minimum <start address> 0x00 and maximum <end address> 0xFF. The <start address> must be less than or equal to the <end address>

You will also be asked to setup the cache properties. The cache size can be from 32 to 256 bytes inclusive. 

The block size can be any value from 1 to the cache size inclusive. The associativity can either be 1, 2, or 4. 

An error will be thrown if associativity makes it so there is not an integer number of sets.

You will also be asked to enter various cache policies. For replacement, 1 is random, 2 is least recently used, and 3 is least frequently used.

For write hit policies, 1 is write-through, and 2 is write-back.

For write miss policies, 1 is write-allocate, and 2 is no-write-allocate. 

Once the cache is successfully configured, you can execute a variety of commands. You can read and write to the cache. You can view and flush the cache.

You can also dump the RAM / cache contents into a text file. Finally, you can also view the RAM contents.

The read and write commands are the only commands that accept arguments. The read command takes in a hexadecimal address.

The write command takes in a hexadecimal address followed by a hexadecimal data value to write.

Enter quit to end the cache simulator
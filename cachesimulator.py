'''
// File: cachesimulator.py
// Author(s): Jacob Enerio
// Date: 12/8/2021
// Section: 505 
// E-mail(s): jacobwde@tamu.edu 
// Description:
// The content of this file implements a cache-simulator for a cache with 8
// address bits.
'''
# Import
import sys
from math import log
from random import randint

def dec2hex(dec):
    '''Converts a decimal value to a hexadecimal value'''
    return hex(dec).upper()

def dec2hexNoX(dec):
    '''Converts a decimal value to a hexadecimal value without the 0x'''
    return dec2hex(dec)[2:]

def hex2dec(hexa):
    '''Converts a hexadecimal value to a decimal value'''
    return int(hexa.lower(), 16)

def hex2bin(hexa):
    '''Converts a hexadecimal value to a binary value'''
    return bin(hex2dec(hexa))

def hex2binNoB(hexa):
    '''Converts a hexadecimal value to a binary value without the 0b'''
    return hex2bin(hexa)[2:]

def bin2dec(bina):
    '''Converts a binary value to a decimal value'''
    return int(bina, 2)

def bin2hex(bina):
    '''Converts a binary value to a hexadecimal value'''
    return dec2hex(bin2dec(bina)) 

def bin2hexNoX(bina):
    '''Converts a binary value to a hexadecimal value without the 0x'''
    return bin2hex(bina)[2:]


class RAM:
    '''Class that stores data in RAM'''
    fileName = ""
    contents = {}
    memorySize = 256
    memoryStart = 0
    memoryEnd = 255
    blockSize = 8
    # Initialize the RAM
    def __init__(self, filename):
        '''Initializes the RAM'''
        super();
        # Reset contents
        self.contents = {}
        self.fileName = filename
        print("*** Welcome to the cache simulator ***")
        valid = False
        # Keep looping until user enters correct value
        while valid == False:
            print("initialize the RAM:")
            uConfigs = input()
            # Get the args
            args = uConfigs.split(" ")
            # Check to make sure first arg is correct
            if args[0] != "init-ram":
                print("Invalid Command:", uConfigs)
                print("Correct format: init-ram <start address> <end address>")
                continue
            if len(args) != 3:
                # init-ram has only 3 arguments
                print("Invalid Command format!")
                print("Correct format: init-ram <start address> <end address>")
                continue
            try: 
                # Ensure argument has a 0x
                if (args[1][0:2] != "0x"):
                    print("Memory addressess must start with 0x!")
                    continue
                # Try to convert argument 1 to an integer
                decStart = hex2dec(args[1].lower())
                # Check to make sure starting address is valid
                if (decStart < 0 or decStart > 255):
                    # Inform the user they are out of range
                    print("Memory addresses are limited to 8 bits from 0x00 to 0xF!F")
                    continue
                # Set the correct memory start position
                self.memoryStart = decStart
            except ValueError:
                # Inform the user they made an error
                print("Start address should be a hexadecimal value!")
            try: 
                # Ensure argument has a 0x
                if (args[2][0:2] != "0x"):
                    print("Memory addressess must start with 0x!")
                    continue
                # Try to convert argument 2 to an integer
                decEnd = hex2dec(args[2].lower())
                # Check to make sure starting address is valid
                if (decEnd < 0 or decEnd > 255):
                    # Inform the user they are out of range
                    print("Memory addresses are limited to 8 bits from 0x00 to 0xFF!")
                    continue
                # Set the correct memory end position
                self.memoryEnd = decEnd
            except ValueError:
                # Inform the user they made an error
                print("End address should be a hexadecimal value!")
                continue
            # Make sure to set correct size 
            self.memorySize = self.memoryEnd - self.memoryStart + 1
            valid = True
            
        self.readFile()
        print("RAM successfully initialized!")
        
    def readFile(self):
        '''Reads a file and adds its content to the RAM'''
        with open(self.fileName) as file:
            print ("Reading file")
            lines = file.readlines()
            # Loop through file and add contents to dictionary
            for i in range(self.memorySize):
                # Make sure no new line character when we get line
                self.contents[i] = lines[i].strip("\n")
            # print(self.contents)
            
    def read(self, address, B):
        '''Reads a line from the RAM'''
        line = []
        # Need to rewrite address so it starts at a block
        startAddress = address - address % B 
        # Need to loop through appropriate addresses
        for i in range(startAddress, startAddress + B):
            # Add the byte to the line if it exists
            if i in self.contents:
                line.append(self.contents[i])
            else:
                # Otherwise append 0
                line.append("00")
        return line
    
    def write(self, address, data):
        '''Writes a byte to the RAM'''
        self.contents[address] = data
        
    def writeLine(self, address, data, B):
        '''Writes a line of bytes to the RAM'''
        startAddress = address - address % B 
        # Loop through block
        for i in range(B):
            if startAddress + i in self.contents:
                # Add content to RAM if allowed
                self.contents[startAddress + i] = data[i]
                # print("Writing",data[i],"to address", startAddress + i)
        
    def view(self):
        '''Displays content of RAM'''
        print("memory_size:", self.memorySize, sep = "")
        print("memory_content:")
        print("address:data")
        # Print the data 
        # for i in range(self.memorySize // self.blockSize):
        for i in range(256 // 8):
            print("0x", dec2hexNoX(i * self.blockSize).rjust(2, '0'), sep = "", end = ":")
            # Print each Byte in the block
            for j in range(self.blockSize - 1):
                if j + self.blockSize * i in self.contents:
                    # Print if object is in ram
                    print(self.contents[j + self.blockSize * i], end = " ")
                else:
                    # Otherwise print 00
                    print("00", end = " ")
            # Print final byte if it exists
            if self.blockSize - 1 + self.blockSize * i in self.contents:
                print(self.contents[self.blockSize - 1 + self.blockSize * i])
            else:
                # Print 00 otherwise
                print("00")
            
    def dump(self):
        '''Dumps contents into ram.txt'''
        with open('ram.txt', 'w') as file:
            # for i in range(self.memoryStart, self.memoryEnd):
            for i in range(0, 255):
                if i in self.contents:
                    # Print contents if it exists
                    file.write(self.contents[i] + "\n")
                else:
                    # Otherwise print 00
                    file.write("00\n")
            # Dump the last byte if it exists
            if 255 in self.contents:
                file.write(self.contents[255])
            else:
                # Otherwise print 00
                file.write("00")
            # Continue until 256
        
            
        
            
class Set:
    '''Class that implements a set for a cache'''
    # Initialize variables
    tags = []
    valids = []
    lines = {}
    # Initialize replacement policy variables
    timesReplaced = []
    lastAccess = []
    accessNum = 0
    # Initialize properties
    blockSize = 0
    numLines = 0
    # Initialize dirty bits
    dirtyBits = []
    # Initialize set identifier
    num = 0
    # Address used for replacing line into ram
    addresses = []
    
    def __init__(self, B, E, num):
        '''Initializes the set'''
        self.blockSize = B
        self.numLines = E
        self.num = num
        # Initialize variables
        self.tags = []
        self.valids = []
        self.lines = {}
        # Initialize replacement policy variables
        self.timesReplaced = []
        self.lastAccess = []
        self.accessNum = 0   
        # Initialize dirty bits
        self.dirtyBits = []
        self.addresses = []
        # E and B set by constructor
        # Initialize the tags, valids
        for i in range(E):
            # Append bits
            self.tags.append(None) 
            self.valids.append(0)
            # Append replacement policiy variables
            self.timesReplaced.append(0)
            self.lastAccess.append(0)
            self.dirtyBits.append(0)
            # Initialize current line
            self.lines[i] = []
            self.addresses.append(0)
            # Initialize lines
            for j in range(B):
                self.lines[i].append("00")
                
    def replaceLine(self, lineNum, newLine):
        self.lines[lineNum] = newLine
        # ("Replacing line", lineNum, "in set", self.num)
        
    
    def getLRULineNum(self):
        '''Gets the line number of the line least recently used'''
        # Initialize variables
        leastAccessed = self.lastAccess[0]
        lineNum = 0
        # Loop through 
        for i in range(1, self.numLines):
            # If a line was used further in the past, then it is the
            # line we are looking for
            if self.lastAccess[i] < leastAccessed:
                leastAccessed = self.lastAccess[i]
                lineNum = i
        return lineNum
    
    def getLFULineNum(self):
        '''Gets the line number of the line least frequently used'''
        # Initialize variables
        leastTimes = self.timesReplaced[0]
        lineNum = 0
        # Loop through 
        for i in range(1, self.numLines):
            # If a line was least used
            if self.timesReplaced[i] < leastTimes:
                leastTimes = self.timesReplaced[i]
                lineNum = i
        return lineNum
    
    def reset(self):
        '''Resets the set to initial values'''
        # Initialize variables
        self.tags = []
        self.valids = []
        self.lines = {}
        # Initialize replacement policy variables
        self.timesReplaced = []
        self.lastAccess = []
        self.accessNum = 0   
        # Initialize dirty bits
        self.dirtyBits = []
        self.addresses = []
        # E and B set by constructor
        # Initialize the tags, valids
        for i in range(self.numLines):
            # Append bits
            self.tags.append(None) 
            self.valids.append(0)
            # Append replacement policiy variables
            self.timesReplaced.append(0)
            self.lastAccess.append(0)
            self.dirtyBits.append(0)
            # Initialize current line
            self.lines[i] = []
            self.addresses.append(0)
            # Initialize lines
            for j in range(self.blockSize):
                self.lines[i].append("00")
        
            
    
            
class Cache:
    '''Class that stores data in a Cache'''
    # Initialize variables
    fileName = ""
    ram = None
    # Initialize cache properties
    cacheSize = 0 # This is C
    dataBlockSize = 0 # This is B 
    associativity = 0 # This is E
    # Initialize cache policies
    replacementPolicy = 0
    writeHitPolicy = 0
    writeMissPolicy = 0
    # Initialize data portion that has sets, lines, and blocks
    sets = []
    # Initialize other Cache variables
    numSets = 0 # This is S
    NUMADDRESSBITS = 8 # This is m (CONSTANT!)
    numSetBits = 0 # This is s
    numBlockBits = 0 # This is b
    numTagBits = 0 # This is t
    # Initialize Cache hit / miss counters
    hitCounter = 0
    missCounter = 0
    # Dictionary that contains replacement policies
    replacementPolicies = {1 : "random_replacement", 2 : "least_recently_used", 3 : "least_frequently_used"}
    hitPolicies = {1 : "write_through", 2 : "write_back"}
    missPolicies = {1 : "write_allocate", 2 : "no_write_allocate"}

    def __init__(self, ram):
        '''Initializes the cache'''
        # Initialize ram
        self.ram = ram
        self.fileName = ram.fileName
        # Tell user to configure cache 
        print("configure the cache:")
        # Setup valid bool
        valid = False
        # Initialize cache properties
        while valid == False:
            try:
                self.cacheSize = int(input("cache size: "))
                # Check for correct cache size
                if self.cacheSize > 256 or self.cacheSize < 8:
                    print("Cache size must be between 8 and 256 bytes inclusive!")
                else:
                    # Cache Size is okay, so exit loop
                    valid = True
            except ValueError:
                # Cache Size is not an integer
                print("Cache Size must be an integer!")
        # Reset valid
        valid = False
        while valid == False:
            try:
                # Get data block size
                self.dataBlockSize = int(input("data block size: "))
                if self.dataBlockSize > self.cacheSize or self.dataBlockSize < 1:
                    # Data Block Size should between 1 and the cache size inclusive
                    print("Data Block Size should be between 1 and", self.cacheSize, "inclusive!")
                else:
                    # Data Block Size is okay
                    valid = True
            except ValueError:
                # Data Block Size is not an integer
                print("Data Block Size must be an integer!")
        # Reset valid
        valid = False
        while valid == False:
            try:
                # Get associativity
                self.associativity = int(input("associativity: "))
                # Ensure that associativity is correct
                if (self.associativity in [1, 2, 4]) == False:
                    # Tell user their input is wrong
                    print("Associativity must be 1, 2, or 4!")
                elif self.cacheSize % (self.associativity * self.dataBlockSize) != 0:
                    # Ensure that number of sets is an integer
                    print("Number of sets is not an integer!")
                    print("Need to make associativity such that number of sets is an integer!")
                else:
                    # User did everything right
                    valid = True
            except ValueError:
                # Associativity is not an integer
                print("Associativity must be an integer!")
        # Initialize cache policies
        # Reset valid
        valid = False
        while valid == False:
            try:    
                # Get the replacement policy
                self.replacementPolicy = int(input("replacement policy: "))
                if self.replacementPolicy < 1 or self.replacementPolicy > 3:
                    # User put invalid replacement policy
                    print("Replacement Policy must be between 1 and 3 inclusive!")
                else:
                    # replacement policy correct
                    valid = True
            except ValueError:
                # Replacement Policy is not an integer
                print("Replacement Policy must be an integer!")
        # Reset valid
        valid = False
        while valid == False:
            try:
                # Get the write hit policy
                self.writeHitPolicy = int(input("write hit policy: "))
                if self.writeHitPolicy < 1 or self.writeHitPolicy > 2:
                    # User put invalid write hit policy
                    print("Write Hit Policy must be between 1 and 2 inclusive!")
                else:
                    # write hit policy correct
                    valid = True
            except ValueError:
                # Write Hit Policy is not an integer
                print("Write Hit Policy must be an integer!")
        # Reset valid
        valid = False
        while valid == False:
            try: 
                # Get Write Hit policy
                self.writeMissPolicy = int(input("write miss policy: "))
                if self.writeMissPolicy < 1 or self.writeMissPolicy > 2:
                    # User put invalid write miss policy
                    print("Write Miss Policy must be between 1 and 2 inclusive!")
                else:
                    # write miss policy correct
                    valid = True
            except ValueError:
                # Write Miss Policy is not an integer
                print("Write Miss Policy must be an integer!")
        
        # Initialize the cache sets
        for i in range(self.cacheSize):
            tempSet = Set(self.dataBlockSize, self.associativity, i)
            self.sets.append(tempSet)
        
        # Initialize other cache variables
        # S = C / (E * B)
        self.numSets = self.cacheSize // (self.associativity * self.dataBlockSize)
        # print(self.numSets)
        # s = log_2(S)
        self.numSetBits = int(log(self.numSets, 2))
        # print(self.numSetBits)
        # b = log_2(B)
        self.numBlockBits = int(log(self.dataBlockSize, 2))
        # print(self.numBlockBits)
        # t = m - (s + b)
        self.numTagBits = self.NUMADDRESSBITS - (self.numSetBits + self.numBlockBits)
        # print(self.numTagBits)
                
        # Inform user cache successfully configured
        print("cache successfully configured!")
        
    def simulate(self):
        '''Simulates cache operations given user input'''
        command = None
        # Unless command is quit, keep simulating
        while (command != "quit"):
            # Print the cache simulator menu
            print("*** Cache simulator menu ***")
            print("type one command:")
            print("1. cache-read")
            print("2. cache-write")
            print("3. cache-flush")
            print("4. cache-view")
            print("5. memory-view")
            print("6. cache-dump")
            print("7. memory-dump")
            print("8. quit")
            print("****************************")
            # Get the command from input
            command = input()
            args = command.split(" ")
            # Execute the command
            self.executeCMD(args)
            
    def executeCMD(self, args):
        '''Executes a command given its arguments'''
        if len(args) == 0:
            # No command, print error
            print("No command given!")
        elif args[0] == "cache-read":
            # Get ram start and end addresses for error checking
            ramStartHex = dec2hex(self.ram.memoryStart)
            ramEndHex = dec2hex(self.ram.memoryEnd)
            # Only 2 arguments in read
            if len(args) != 2:
                print("Incorrect command format!")
                print("Correct Command format: cache-read <address>")    
            else:
                # Check 2nd argument
                # Ensure there is a 0x
                if args[1][0:2] != "0x":
                    print("<address> must start with a 0x!")
                    return
                # Try to convert value
                try:
                    temp = int(args[1], 16)
                    # Ensure that the ram has the address
                    if temp < self.ram.memoryStart or temp > self.ram.memoryEnd:
                        print("<address> must be between", ramStartHex, "and", ramEndHex, "inclusive!")
                        return
                except ValueError:
                    print("<address> should be a hexadecimal value!")
                    return
                # Read if okay
                self.read(args[1])
        elif args[0] == "cache-write":
            # Get ram start and end addresses for error checking
            ramStartHex = dec2hexNoX(self.ram.memoryStart)
            ramEndHex = dec2hexNoX(self.ram.memoryEnd)
            # Only 3 arguments in write
            if len(args) != 3:
                print("Incorrect command format!")
                print("Correct Command format: cache-write <address> <data>")    
            else:
                # Check 2nd argument
                # Ensure there is a 0x
                if args[1][0:2] != "0x":
                    print("<address> must start with a 0x!")
                    return
                # Try to convert value
                try:
                    temp = int(args[1], 16)
                    # Ensure that the ram has the address
                    if temp < self.ram.memoryStart or temp > self.ram.memoryEnd:
                        print("<address> must be between", "0x" + ramStartHex.rjust(2, '0'), end = "")
                        print(" and", "0x" + ramEndHex.rjust(2, '0'), "inclusive!")
                        return
                except ValueError:
                    print("<address> should be a hexadecimal value!")
                    return
                # Check 3rd argument
                # Ensure there is a 0x
                if args[2][0:2] != "0x":
                    print("<data> must start with a 0x!")
                    return
                # Try to convert value
                try:
                    temp = int(args[2], 16)
                    # Ensure that the ram has the address
                    if temp < 0 or temp > 255:
                        print("<data> must be between 0x00 and 0xFF inclusive!")
                        return
                except ValueError:
                    print("<data> should be a hexadecimal value!")
                    return
                # Write if okay
                self.write(args[1], args[2])
        elif args[0] == "cache-flush":
            # Only 1 argument in flush
            if len(args) != 1:
                print("Incorrect command format!")
                print("Correct Command format: cache-flush")
            else:
                self.flush()
        elif args[0] == "cache-view":
            # Only 1 argument in cache-view
            if len(args) != 1:
                print("Incorrect command format!")
                print("Correct Command format: cache-view")
            else:
                self.view()
        elif args[0] == "memory-view":
            # Only 1 argument in memory-view
            if len(args) != 1:
                print("Incorrect command format!")
                print("Correct Command format: memory-view")
            else:
                self.ram.view()
        elif args[0] == "cache-dump":
            # Only 1 argument in cache-dump
            if len(args) != 1:
                print("Incorrect command format!")
                print("Correct Command format: cache-dump")
            else:
                self.dump()
        elif args[0] == "memory-dump":
            # Only 1 argument in memory-dump
            if len(args) != 1:
                print("Incorrect command format!")
                print("Correct Command format: memory-dump")
            else:
                self.ram.dump()
        elif args[0] == "quit":
            # No need to do anything, just quit
            return 
        else:
            # Invalid command: Error
            print("Invalid command:",args[0])
            
    def read(self, hexAddress):
        '''Reads an adddress from the cache if possible. Otherwise reads from
        memory'''
        # Get the address in binary and decimal
        binAddress = hex2binNoB(hexAddress).rjust(self.NUMADDRESSBITS, '0')
        address = hex2dec(hexAddress)
        # For ease of access use shorter variable names
        t = self.numTagBits
        s = self.numSetBits
        b = self.numBlockBits
        
        # Get the tag, set, and block bits from the binary address
        binTag = binAddress[0:t]
        binSet = binAddress[t:t + s]
        binBlock = binAddress[t + s:t + s + b]
        
        # Convert the tag bits to hexadecimal
        hexTag = bin2hexNoX(binTag)
        # Convert the set index to decimal
        if len(binSet) != 0:
            # More than 1 set
            decSet = bin2dec(binSet)
        else:
            # Handle case where only 1 set
            decSet = 0
        # Convert the block offset to decimal 
        decBlock = bin2dec(binBlock)
        
        # Go through and see if we have the address 
        theSet = self.sets[decSet]
        cacheHit = False
        evictedLine = 0
        byteReturned = ""
        doPolicy = True
        # Loop through all lines
        for i in range(self.associativity):
            tag = theSet.tags[i]
            # If there is no tag, there is no line, add to set
            if tag == None:
                # Need to read from memory to add
                line = self.ram.read(address, self.dataBlockSize)
                theSet.replaceLine(i, line) 
                # Set address
                theSet.addresses[i] = address
                byteReturned = line[decBlock]
                # Need to make valid bit now
                theSet.valids[i] = 1
                # Need to set the tag to the correct place
                theSet.tags[i] = hexTag
                # No need to do policy
                doPolicy = False
                # Read complete - break and set evicted line
                evictedLine = i
                break
            # If tag matches, need to check valid tag
            elif tag == hexTag:
                if theSet.valids[i] == 1:
                    # We have a cache hit
                    cacheHit = True
                    # Get the byte
                    byteReturned = theSet.lines[i][decBlock]
                    # No need to do policy
                    doPolicy = False
                    # Need to update evictedLine for policies
                    evictedLine = i
                    break
                
        # If policy needed, need to evict line using replacement policy
        if doPolicy == True:
            if self.replacementPolicy == 1:
                # Perform random replacement
                evictedLine = randint(0, self.associativity) 
            elif self.replacementPolicy == 2:
                evictedLine = theSet.getLRULineNum()
            else:
                evictedLine = theSet.getLFULineNum()
            # If line is dirty, need to write it to the ram since ram is not updated
            if theSet.dirtyBits[evictedLine] == 1:
                # Get address of line to be evicted
                self.ram.writeLine(theSet.addresses[evictedLine], theSet.lines[evictedLine], self.dataBlockSize)
                # Set dirty bit to 0
                theSet.dirtyBits[evictedLine] = 0
            # Now read from memory
            line = self.ram.read(address, self.dataBlockSize)
            theSet.lines[evictedLine] = line 
            # Set address
            theSet.addresses[evictedLine] = address
            byteReturned = line[decBlock]
            # Need to make valid bit now
            theSet.valids[evictedLine] = 1
            # Need to set the tag to the correct place
            theSet.tags[evictedLine] = hexTag
                
        # Print the results of the read
        print("set:", decSet, sep = "")
        print("tag:", hexTag.rjust(2, '0'), sep = "")
        if cacheHit == True:
            # Print appropriate statements for cache hit
            print("hit:yes")
            print("eviction_line:-1")
            print("ram_address:-1")
            self.hitCounter += 1
        else:
            # Print appropriate statements for cache miss   
            print("hit:no")
            print("eviction_line:", evictedLine, sep = "")
            print("ram_address:", hexAddress, sep = "")
            self.missCounter += 1
        # Print byte returned
        print("data:0x", byteReturned, sep = "")
                
        # Update set properties
        theSet.accessNum += 1
        theSet.lastAccess[evictedLine] = theSet.accessNum
        theSet.timesReplaced[evictedLine] += 1
    
    def write(self, hexAddress, data):
        '''Writes data to an adddress from the cache if possible. Writes to
        memory. Also relies on write policy'''
        # Get the address in binary and decimal
        binAddress = hex2binNoB(hexAddress).rjust(self.NUMADDRESSBITS, '0')
        address = hex2dec(hexAddress)
        # Get the data without the 0x
        dataNoX = data[2:]
        # For ease of access use shorter variable names
        t = self.numTagBits
        s = self.numSetBits
        b = self.numBlockBits
        
        # Get the tag, set, and block bits from the binary address
        binTag = binAddress[0:t]
        binSet = binAddress[t:t + s]
        binBlock = binAddress[t + s:t + s + b]
        
        # Convert the tag bits to hexadecimal
        hexTag = bin2hexNoX(binTag)
        # Convert the set index to decimal
        if len(binSet) != 0:
            # More than 1 set
            decSet = bin2dec(binSet)
        else:
            # Handle case where only 1 set
            decSet = 0
        # Convert the block offset to decimal 
        decBlock = bin2dec(binBlock)
        
        # Go through and see if we have the address 
        theSet = self.sets[decSet]
        cacheHit = False
        evictedLine = 0
        byteReturned = ""
        doPolicy = True
        dirty = 0
        # Loop through all lines
        for i in range(self.associativity):
            tag = theSet.tags[i]
            # If there is no tag, there is no line, add to set
            if tag == None:
                # If write allocate, need to load from ram and put it in cache
                if self.writeMissPolicy == 1:
                    # Need to read from memory to add
                    line = self.ram.read(address, self.dataBlockSize)
                    theSet.lines[i] = line 
                    # Set address
                    theSet.addresses[i] = address
                    byteReturned = line[decBlock]
                    # Write the data to the correct location in the line
                    theSet.lines[i][decBlock] = dataNoX
                    # write-allocate requires followup by the write-hit action
                    # if write-through, need to write the data to the RAM
                    if self.writeHitPolicy == 1:
                        self.ram.write(address, dataNoX)
                        theSet.dirtyBits[i] = 0
                        dirty = 0
                    # Otherwise if write-back, need to set dirty bit
                    if self.writeHitPolicy == 2:
                        theSet.dirtyBits[i] = 1
                        dirty = 1
                    # Only applies to write-allocate
                    # Need to make valid bit now
                    theSet.valids[i] = 1
                    # Need to set the tag to the correct place
                    theSet.tags[i] = hexTag
                # If not write allocate, need to write to RAM but not cache
                else:
                    self.ram.write(address, dataNoX)
                    byteReturned = dataNoX
                    # Handle Dirty bit
                    # theSet.dirtyBits[i] = 0
                    dirty = theSet.dirtyBits[evictedLine]
                # No need to do policy
                doPolicy = False
                # Read complete - break and set evicted line
                evictedLine = i
                break
            # If tag matches, need to check valid tag
            elif tag == hexTag:
                if theSet.valids[i] == 1:
                    # We have a cache hit
                    cacheHit = True
                    # Get the byte
                    byteReturned = theSet.lines[i][decBlock]
                    # Write the data to the cache
                    theSet.lines[i][decBlock] = dataNoX
                    # if write-through, need to write the data to the RAM
                    if self.writeHitPolicy == 1:
                        self.ram.write(address, dataNoX)
                        theSet.dirtyBits[i] = 0
                        dirty = 0
                    # Otherwise if write-back, need to set dirty bit
                    if self.writeHitPolicy == 2:
                        theSet.dirtyBits[i] = 1
                        dirty = 1
                    # No need to do policy
                    doPolicy = False
                    # Need to update evictedLine for policies
                    evictedLine = i
                    break
                
        # If policy needed, need to evict line using replacement policy
        if doPolicy == True:
            if self.replacementPolicy == 1:
                # Perform random replacement
                evictedLine = randint(0, self.associativity) 
            elif self.replacementPolicy == 2:
                evictedLine = theSet.getLRULineNum()
            else:
                evictedLine = theSet.getLFULineNum()
            # If line is dirty, need to write it to the ram since ram is not updated
            if theSet.dirtyBits[evictedLine] == 1:
                # Get address of line to be evicted
                self.ram.writeLine(theSet.addresses[evictedLine], theSet.lines[evictedLine], self.dataBlockSize)
                # Set dirty bit to 0
                theSet.dirtyBits[evictedLine] = 0
            # If write allocate, need to load from ram and put it in cache
            if self.writeMissPolicy == 1:
                # Need to read from memory to add
                line = self.ram.read(address, self.dataBlockSize)
                theSet.lines[evictedLine] = line 
                # Set address
                theSet.addresses[evictedLine] = address
                byteReturned = line[decBlock]
                # Write the data to the correct location in the line
                theSet.lines[evictedLine][decBlock] = dataNoX
                # if write-through, need to write the data to the RAM
                # write-allocate requires followup by the write-hit action
                if self.writeHitPolicy == 1:
                    self.ram.write(address, dataNoX)
                    theSet.dirtyBits[evictedLine] = 0
                    dirty = 0
                # Otherwise if write-back, need to set dirty bit
                if self.writeHitPolicy == 2:
                    theSet.dirtyBits[evictedLine] = 1
                    dirty = 1
            # If not write allocate, need to write to RAM but not cache
            else:
                self.ram.write(address, dataNoX)
                byteReturned = dataNoX
                # Dirty bit is unchanged
                dirty = theSet.dirtyBits[evictedLine]
            # Need to make valid bit now
            theSet.valids[evictedLine] = 1
            # Need to set the tag to the correct place
            theSet.tags[evictedLine] = hexTag
                
        # Print the results of the read
        print("set:", decSet, sep = "")
        print("tag:", hexTag.rjust(2, '0'), sep = "")
        if cacheHit == True:
            # Print appropriate statements for cache hit
            print("write_hit:yes")
            print("eviction_line:-1")
            print("ram_address:-1")
            self.hitCounter += 1
        else:
            # Print appropriate statements for cache miss   
            print("write_hit:no")
            print("eviction_line:", evictedLine, sep = "")
            print("ram_address:", hexAddress, sep = "")
            self.missCounter += 1
        # Print byte returned
        print("data:", data, sep = "")
        # Print dirty bit
        print("dirty_bit:", dirty, sep = "" )
                
        # Update set properties
        theSet.accessNum += 1
        theSet.lastAccess[evictedLine] = theSet.accessNum
        theSet.timesReplaced[evictedLine] += 1
                
    def flush(self):
        '''Clears the cache'''
        self.hitCounter = 0
        self.missCounter = 0
        # Reset all sets
        for i in range(self.numSets):
            self.sets[i].reset()
    
    def view(self):
        '''Prints the cache settings and contents to the console'''
        # Main Cache Properties
        print("cache_size:", self.cacheSize, sep = "")
        print("data_block_size:", self.dataBlockSize, sep = "")
        print("associativity:", self.associativity, sep = "")
        # Cache Policies
        print("replacement_policy:", self.replacementPolicies[self.replacementPolicy], sep = "")
        print("write_hit_policy:", self.hitPolicies[self.writeHitPolicy], sep = "")
        print("write_miss_policy:", self.missPolicies[self.writeMissPolicy], sep = "")
        # Cache Hits / Misses
        print("number_of_cache_hits:", self.hitCounter, sep = "")
        print("number_of_cache_misses:", self.missCounter, sep = "")
        # Display cache data
        for i in range(self.numSets):
            theSet = self.sets[i]
            # Display each line in the set
            for j in range(self.associativity):
                # Display bits
                # print("Printing line", j, "from set", theSet.num, end = ": ")
                print(theSet.valids[j], theSet.dirtyBits[j], end = " ")
                
                # Print the tag
                theTag = theSet.tags[j]
                if (theTag == None):
                    # Set None to 0 tag
                    theTag = "00"
                print(theTag.rjust(2,'0'), end = " ")
                theLine = theSet.lines[j]
                # Print the block 
                for k in range(self.dataBlockSize - 1):
                    print(theLine[k], end = " ")
                # Print the final byte
                print(theLine[self.dataBlockSize - 1])
                
    def dump(self):
        '''Dumps the cache contents into cache.txt'''
        # Open File
        with open("cache.txt", 'w') as file:
            for i in range(self.numSets):
                theSet = self.sets[i]
                # Display each line in the set
                for j in range(self.associativity):
                    theLine = theSet.lines[j]
                    # Print the block 
                    for k in range(self.dataBlockSize - 1):
                        file.write("{} ".format(theLine[k]))
                    # Print the final byte
                    file.write("{}\n".format(theLine[self.dataBlockSize - 1]))
                

        
        

        
        

        


def main():
    '''Main function executed when program is ran'''
    # Get the name of the file
    # print ("Main entered")
    fileName = sys.argv[1]
    #print(fileName)

    # Initialize the RAM
    ram = RAM(fileName)
    
    # Initialize the Cache
    cache = Cache(ram)
    cache.simulate()
    return 0


if __name__ == "__main__":
    main()
    

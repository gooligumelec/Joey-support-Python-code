#!/usr/bin/python
#
# IP address display for Raspberry Pi boards
#
# Written by S G OBrien  April - June 2015.
# modified by David Meiklejohn (Gooligum Electronics)
#
#   v1.3    12/11/15
#
# THIS CODE CANNOT BE USED OR REPRODUCED WITHOUT PERMISSION FROM THE AUTHORS
# COPYRIGHT 2015.
#----------------------------------------------------------------------------

import time
import os
from joey_support import joeyBoard
# ===========================================================================

# initialise Joey board
display = joeyBoard()

print "IP Address Display 4 digit 7 segment display module"

# get first valid IP address line from ifconfig
address = os.popen('ifconfig | grep "inet addr" | grep -v 127.0.0.1').readline()

# extract the address characters
adr1 = address
#split out the ip address, whitespace is the delimiter
a,b,c,d=adr1.split()
#remove the characters in front of the IP address numbers
adr1=b[5:]
#split out the four components of the ip address, '.' is the delimiter
adr1.split('.')
a,b,c,d=adr1.split('.')
a = int(a)
b = int(b)
c = int(c)
d = int(d)
print "IP address is :", a, b, c, d

# paus is a function that pauses between each number and
# displays "dot" so you can tell if the IP address has two numbers the same
def paus():
    time.sleep(3)
    display.writeWord("dot ")  
    time.sleep(1)

# display "Addr" to show we've started
display.writeWord("Addr")  
time.sleep(1)

# write IP address to the diplay
#1st address number (a)
display.writeInt(a)

#2nd address number (b)
paus()
display.writeInt(b)

#3rd address number (c)
paus()
display.writeInt(c)

#4th address number (d)
paus()
display.writeInt(d)
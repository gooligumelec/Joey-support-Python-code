#!/usr/bin/python
#
# Display a text message as a series of words on the Joey
#
#   v1.0    11/11/15
#
#   David Meiklejohn
#   Gooligum Electronics

import time
from joey_support import joeyBoard

# initialise the display
display = joeyBoard()

# the text to display (each word should be <= 4 chars)
text = "HEL0 MY NAME IS J0EY"

# split the text into words
words = text.split()

# display them
for w in words:
    display.writeWord(w)
    time.sleep(1)           # pause 1 sec between words

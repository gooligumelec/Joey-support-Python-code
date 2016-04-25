#!/usr/bin/python
#
# Counter
#
# Displays counts of off->on transitions of JP3 input on Joey board
#
# Count resets when JP2 is closed
#
#   v1.0    24/04/16
#
#   David Meiklejohn
#   Gooligum Electronics
#

import time

from joey_support import joeyBoard

# initialise Joey board
display = joeyBoard()

count = 0
display.writeInt(count)   

try:
  while True:
    # wait for JP3 to open
    while display.getJumpers() & 4 == 4:
      if display.getJumpers() & 2:  # reset count if JP2 closed
        count = -1
        break
      time.sleep(0.2)               # 200ms debounce delay
    # wait for JP3 to close
    while display.getJumpers() & 4 == 0:
      if display.getJumpers() & 2:  # reset count if JP2 closed
        count = -1
        break
      time.sleep(0.2)               # 200ms debounce delay
    count += 1
    # display count
    display.writeInt(count)   

except KeyboardInterrupt:
  display.disp.clear()    #clear display on exit

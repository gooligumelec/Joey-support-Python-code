#!/usr/bin/python
#
# Counter
#
# Displays counts of off->on transitions of JP3 input on Joey board
#
# Count resets when JP2 is closed
#
#   v1.1    24/04/16
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
    # wait for JP3 to remain open
    db_cnt = 0
    while db_cnt < 10:
      if display.getJumpers() & 2:  # reset count if JP2 closed
        count = -1
        break
      # increment debounce count while JP3 is open
      if display.getJumpers() & 4 == 0:
        db_cnt += 1
      else:
        db_cnt = 0
      time.sleep(0.01)                 # debounce delay

    # wait for JP3 to close
    db_cnt = 0
    while db_cnt < 2:
      if display.getJumpers() & 2:  # reset count if JP2 closed
        count = -1
        break
      # increment debounce count while JP3 is closed
      if display.getJumpers() & 4 == 4:
        db_cnt += 1
      else:
        db_cnt = 0
      time.sleep(0.01)                 # debounce delay

    # increment and display count
    count += 1
    display.writeInt(count)   

except KeyboardInterrupt:
  display.disp.clear()    #clear display on exit

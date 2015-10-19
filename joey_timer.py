#!/usr/bin/python
#
# Simple Timer
#
# Continually counts up from zero,
#  displaying elapsed time in 0.1 sec
#  on Joey board
#
#   v1.1    19/10/15
#
#   David Meiklejohn
#   Gooligum Electronics
#

import time
from joey_support import joeyBoard

# initialise Joey board
display = joeyBoard()

try:
  while True:
    # count from 0 to 9999
    # (equivalent to 0.0 to 999.9)
    for x in range(10000):
      display.writeValue(x/10.0, 1)         # 1 decimal place

      time.sleep(0.1)    # delay 0.1 sec

except KeyboardInterrupt:
  display.disp.clear()    #clear display to start


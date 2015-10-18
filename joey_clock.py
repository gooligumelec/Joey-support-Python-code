#!/usr/bin/python

import time
import datetime
from joey_support import joeyBoard

# ===========================================================================
# Clock Example
# ===========================================================================
display = joeyBoard(address=0x70)

print "Press CTRL+Z to exit"

# Continually update the time on the "Joey" 4 char, 7-segment display
while(True):
  now = datetime.datetime.now()
  hour = now.hour
  minute = now.minute
  second = now.second
  # Set hours
  display.writeDigit(1, int(hour / 10))     # Tens
  display.writeDigit(2, hour % 10)          # Ones
  # Set minutes
  display.writeDigit(3, int(minute / 10))   # Tens
  display.writeDigit(4, minute % 10)        # Ones
  # Toggle colon
  display.setColon(second % 2)              # Toggle colon at 1Hz
  # Wait one second
  time.sleep(1)

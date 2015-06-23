#!/usr/bin/python
#
# Joey board support modules
#
#   Based on Adafruit_LEDBackpack.py module
#   7-segment display class modified to support "Joey" 4-digit display
#   Functions added to read jumper settings on Joey board
#   v1.0    19/6/15
#
#   David Meiklejohn
#   Gooligum Electronics

import time
from HT16K33 import HT16K33

# ===========================================================================
# Joey board - access to display and jumpers
# ===========================================================================

class joeyBoard:
  disp = None
 
  # Hexadecimal character lookup table (row 1 = 0..9, row 2 = 5..9, row 3 = A..F)
  pattern = [ 0x3027, 0x0006, 0x3043, 0x2047, 0x0066, \
              0x2065, 0x3065, 0x0007, 0x3067, 0x2067, \
              0x1067, 0x3064, 0x3021, 0x3046, 0x3061, 0x1061 ]

  # Column lookup table (digit 1 .. digit 4)
  column = [ 1, 5, 7, 0 ]

  # Constructor
  def __init__(self, address=0x70, debug=False):
    if (debug):
      print "Initializing a new instance of HT16K33 display board at 0x%02X" % address
    self.disp = HT16K33(address=address, debug=debug)

  def writeDigitRaw(self, colval, rowval):
    "Displays a digit using the raw 16-bit row pattern value"
    if (colval > 7):
      return
    # Set the appropriate digit
    self.disp.setBufferRow(colval, rowval)

  def writeDigit(self, digit, value, dot=False):
    "Displays a single hexademical value (0..9 and A..F) on specified digit"
    if (digit > 4):
      return
    if (value > 0xF):
      return
    # Set the appropriate digit
    self.disp.setBufferRow(self.column[digit-1], self.pattern[value] | (dot << 11))

  def setColon(self, state=True):
    "Enables or disables the colon character"
    # Warning: This function assumes that the colon is on COM6
    # which is the case for the Joey display, but may need to be modified
    # if another display type is used
    if (state):
      self.disp.setBufferRow(6, 0xFFFF)
    else:
      self.disp.setBufferRow(6, 0)

  def getJumpers(self):
    "Returns current jumper settings as a 3-bit value (JP1:JP3)"
    # read key data once to clear old jumper settings
    self.disp.getKeys(0)
    time.sleep(0.025)    # delay 25ms between reads (due to 20ms debounce time)
    # read keys again - jumper status is in bits 10:8
    return (self.disp.getKeys(0) >> 8)


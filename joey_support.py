#!/usr/bin/python
#
# Joey board support modules
#
#   Based on Adafruit_LEDBackpack.py module
#   7-segment display class modified to support "Joey" 4-digit display
#   Functions added to read jumper settings on Joey board
#   Character patterns extended to all letters (0-9, A-Z, space)
#   writeChar and writeWord methods added            7/10/15
#   setDP, writeInt and writeValue methods added    19/10/15
#   v1.3    19/10/15
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
 
  # Character pattern lookup table
  pattern = [ 0x3027, 0x0006, 0x3043, 0x2047, 0x0066,           # 0..4  \
              0x2065, 0x3065, 0x0007, 0x3067, 0x2067,           # 5..9  \
              0x1067, 0x3064, 0x3021, 0x3046, 0x3061, 0x1061,   # A..F  \
              0x2067, 0x1066, 0x0006, 0x3006, 0x3062,           # G..K  \
              0x3020, 0x1044, 0x1027, 0x3044, 0x1063,           # L..P  \
              0x0067, 0x1040, 0x2065, 0x3060, 0x3026,           # Q..U  \
              0x3026, 0x3004, 0x1066, 0x2066, 0x3043,           # V..Z  \
              0x0000, 0x0040 ]                                  # space, '-'


  # Column lookup table (digit 1 .. digit 4)
  column = [ 1, 5, 7, 0 ]

  # Constructor
  def __init__(self, address=0x70, debug=False):
    if (debug):
      print("Initializing a new instance of HT16K33 display board at 0x%02X" % address)
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

  def setDP(self, digit, dot=True):
    "Enables or disables the decimal point on specified digit"
    if (digit > 4):
      return
    # get the current pattern displayed on this digit, with DP cleared (bit 11)
    currpat = self.disp.getBufferRow(self.column[digit-1]) & ~(1<<11)
    # write new pattern with DP optionally set
    self.disp.setBufferRow(self.column[digit-1], currpat | (dot << 11))

  def writeChar(self, digit, char, dot=False):
    "Displays a single character (0..9, A..Z, space, -) on specified digit"
    if (digit > 4):
      return
    # get index into pattern table
    try:
      patidx = ('0123456789abcdefghijklmnopqrstuvwxyz -').index(char[0].lower())
    except (ValueError, IndexError):
      return
    # Set the appropriate digit
    self.disp.setBufferRow(self.column[digit-1], self.pattern[patidx] | (dot << 11))

  def writeWord(self, word):
    "Displays a word (up to 4 chars), right-justified, space padded"
    # trim word to 4 digits and pad it
    word=(4*' '+word[:4])[-4:]
    # display it
    for x in range(4):
      self.writeChar(x+1, word[x])

  def writeInt(self, value):
    "Displays a rounded integer value (up to 4 digits), right-justified, space padded"
    # convert value to text string
    text = str(int(round(value)))
    if len(text) > 4:
      text = 'over'
    # trim text to 4 digits and pad it
    text=(4*' '+text[:4])[-4:]
    # display it
    self.writeWord(text)

  def writeValue(self, value, places=0):
    "Displays a rounded value (up to 4 digits) to specified decimal places (max 3), space padded"
    # limit max decimal places
    if value < 0 and places > 2:
      places = 2 
    if value >= 0 and places > 3:
      places = 3
    # display rounded value
    self.writeInt(value*10**places)
    # turn on DP dot
    if places > 0:
      self.setDP(4-places)

  def setColon(self, state=True):
    "Enables or disables the colon character"
    # Warning: This function assumes that the colon is on COM6
    # which is the case for the Joey display, but may need to be modified
    # if another display type is used
    if (state):
      self.disp.setBufferRow(6, 0xFFFF)
    else:
      self.disp.setBufferRow(6, 0)

  def setDegrees(self, state=True):
    "Enables or disables the degrees symbol"
    # Warning: This function assumes that the degrees symbol is on COM4
    # which is the case for the Joey display, but may need to be modified
    # if another display type is used
    if (state):
      self.disp.setBufferRow(4, 0xFFFF)
    else:
      self.disp.setBufferRow(4, 0)

  def getJumpers(self):
    "Returns current jumper settings as a 3-bit value (JP3:JP1)"
    # read key data once to clear old jumper settings
    self.disp.getKeys(0)
    time.sleep(0.025)    # delay 25ms between reads (due to 20ms debounce time)
    # read keys again - jumper status is in bits 10:8
    return (self.disp.getKeys(0) >> 8)


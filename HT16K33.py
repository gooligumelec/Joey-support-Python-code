#!/usr/bin/python
#
# Driver for Holtek HT16K33
#
# Based on Adafruit_LEDBackpack/Adafruit_LEDBackpack.py
# Added getKeys() method to read raw key presses recorded by HT16K33 keyscan
#   v1.1    19/10/15
#
#   David Meiklejohn
#   Gooligum Electronics

import time
from copy import copy
from Adafruit_I2C import Adafruit_I2C

# ============================================================================
# HT16K33 Class
# ============================================================================

class HT16K33:
  i2c = None

  # Registers
  __HT16K33_REGISTER_DISPLAY_SETUP        = 0x80
  __HT16K33_REGISTER_SYSTEM_SETUP         = 0x20
  __HT16K33_REGISTER_DIMMING              = 0xE0

  # Data base addresses
  __HT16K33_ADDRESS_KEY_DATA              = 0x40

  # Blink rate
  __HT16K33_BLINKRATE_OFF                 = 0x00
  __HT16K33_BLINKRATE_2HZ                 = 0x01
  __HT16K33_BLINKRATE_1HZ                 = 0x02
  __HT16K33_BLINKRATE_HALFHZ              = 0x03

  # Display buffer (8x16-bits)
  __buffer = [0x0000, 0x0000, 0x0000, 0x0000, \
              0x0000, 0x0000, 0x0000, 0x0000 ]

  # Constructor
  def __init__(self, address=0x70, debug=False):
    self.i2c = Adafruit_I2C(address)
    self.address = address
    self.debug = debug

    # Turn the oscillator on
    self.i2c.write8(self.__HT16K33_REGISTER_SYSTEM_SETUP | 0x01, 0x00)

    # Turn blink off
    self.setBlinkRate(self.__HT16K33_BLINKRATE_OFF)

    # Set maximum brightness
    self.setBrightness(15)

    # Clear the screen
    self.clear()

  def setBrightness(self, brightness):
    "Sets the brightness level from 0..15"
    if (brightness > 15):
      brightness = 15
    self.i2c.write8(self.__HT16K33_REGISTER_DIMMING | brightness, 0x00)

  def setBlinkRate(self, blinkRate):
    "Sets the blink rate"
    if (blinkRate > self.__HT16K33_BLINKRATE_HALFHZ):
       blinkRate = self.__HT16K33_BLINKRATE_OFF
    self.i2c.write8(self.__HT16K33_REGISTER_DISPLAY_SETUP | 0x01 | (blinkRate << 1), 0x00)

  def setBufferRow(self, row, value, update=True):
    "Updates a single 16-bit entry in the 8*16-bit buffer"
    if (row > 7):
      return                    # Prevent buffer overflow
    self.__buffer[row] = value  # value # & 0xFFFF
    if (update):
      self.writeDisplay()       # Update the display

  def getBufferRow(self, row):
    "Returns a single 16-bit entry in the 8*16-bit buffer"
    if (row > 7):
      return
    return self.__buffer[row]

  def getBuffer(self):
    "Returns a copy of the raw buffer contents"
    bufferCopy = copy(self.__buffer)
    return bufferCopy
 
  def writeDisplay(self):
    "Updates the display memory"
    bytes = []
    for item in self.__buffer:
      bytes.append(item & 0xFF)
      bytes.append((item >> 8) & 0xFF)
    self.i2c.writeList(0x00, bytes)

  def clear(self, update=True):
    "Clears the display memory"
    self.__buffer = [ 0, 0, 0, 0, 0, 0, 0, 0 ]
    if (update):
      self.writeDisplay()

  def getKeys(self, row):
    "Returns a row of scanned key values as a single 13-bit value (K13:K1)"
    if (row > 2):
      return
    return self.i2c.readU16(self.__HT16K33_ADDRESS_KEY_DATA + row*2)


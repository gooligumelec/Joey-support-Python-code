#!/usr/bin/python
#
# CPU temperature display
#
# Continually displays CPU temperature in 
#  in degrees Celsius
#  on Joey board
#
#   v1.1    23/10/15
#
#   David Meiklejohn
#   Gooligum Electronics
#

import os
import time
from joey_support import joeyBoard

# initialise Joey board
display = joeyBoard()
display.setDegrees(True)    # turn on the degrees symbol

try:
  while True:
    # get CPU temperature
    # average 10 successive readings to smooth result
    sum = 0.0
    for x in range(10):
      res = os.popen('vcgencmd measure_temp').readline()
      sum += float(res.replace("temp=","").replace("'C\n",""))
      time.sleep(0.1)
    TempC = sum/10.0
    TempF = TempC * 9/5 + 32

    # select Celsius or Fahrenheit
    # (Celsius if JP1 is closed)
    if display.getJumpers() & 1:
      t = TempC
      dp = 2                        # display 2 decimal place
      unit = 'C'                    # so that 'C' can overwrite 2nd decimal
    else:
      t = TempF*10                  # add a '0'
      dp = 0                        # with no decimal point
      unit = 'F'                    # so that 'F' can overwrite last digit

    # display value
    display.writeValue(t, dp)   
    display.writeChar(4, unit)      # display unit character


except KeyboardInterrupt:
  display.disp.clear()    #clear display on exit


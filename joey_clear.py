#!/usr/bin/python
#
# Clear the Joey display
#
#   v1.0    19/10/15
#
#   David Meiklejohn
#   Gooligum Electronics

from joey_support import joeyBoard

display = joeyBoard(address=0x70)

display.disp.clear()


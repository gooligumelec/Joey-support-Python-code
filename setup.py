from distutils.core import setup

setup(name 				= 'Joey_support',
	  version 			= '1.0.0',
	  author			= 'David Meiklejohn',
	  author_email		= 'support@gooligum.com',
	  description		= 'Library to drive Joey 4-digit 7-seg LED display for Raspberry Pi',
	  license			= 'MIT',
	  url				= 'https://github.com/gooligumelec/Joey-support-Python-code',
	  py_modules        = ['Adafruit_I2C', 'HT16K33', 'joey_support'],
      )


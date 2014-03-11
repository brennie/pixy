#!/usr/bin/env python3.3

from pixy import PixyApp
from pixy.models import User

import os
import sys

##
# \brief Read an option from standard input
# \param prompt The prompt
# \param parser The parser to use to parse the read the inputted ata
# \param default The default value
# \return The parsed value
def read_option(prompt, parser=None, default=None):
	if default is not None:
		print('{0}: (default: {1})'.format(prompt, default))
	else:
		print('{0}: '.format(prompt))

	value = input('> ')
	
	if not len(value) and default is not None:
		return default

	if parser:
		return parser(value)

	return value

if __name__ == '__main__':
	config = {}

	admin_name = read_option('Admin username')
	admin_email = read_option('Admin email')
	admin_pass = read_option('Admin password')

	config['DB_URI'] = read_option('Database URI')
	config['DB_USER'] = read_option('Database username')
	config['DB_PASS'] = read_option('Database password')

	# Secret key for sessions
	config['SECRET_KEY'] = os.urandom(32)

	with open('pixy/pixy.cfg', 'w') as cfg:
		for option, value in config.items():
			cfg.write('{0}={1}\n'.format(option, repr(value)))

	app = PixyApp()
	app.db.create_all()

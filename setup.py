#!/usr/bin/env python3.3

from pixy import PixyApp
from pixy.models import db, User

import os
import stat

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

	print('Database configuration:')
	hostname = read_option('Database hostname')
	dbname = read_option('Database name')
	username = read_option('Database username')
	password = read_option('Database password')

	config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(username, password, hostname, dbname)

	# Secret key for sessions
	config['SECRET_KEY'] = os.urandom(32)

	with open('pixy/pixy.cfg', 'w') as cfg:
		for option, value in config.items():
			cfg.write('{0}={1}\n'.format(option, repr(value)))

	os.chmod('pixy/pixy.cfg', 0o600)

	app = PixyApp()
	with app.app_context():
		db.create_all()

		print('Add administrators:')
		nAdmins = read_option('Number of administrators', int, 1)
		for i in range(0, nAdmins):
			admin_name = read_option('Admin username')
			while not User.validate_username(admin_name):
				print('Invalid username')
				admin_name = read_option('Admin username')

			admin_email = read_option('Admin email')
			while not User.validate_email(admin_email):
				print('Invalid email')
				admin_email = read_option('Admin email')

			admin_pass = read_option('Admin password')
			while not User.validate_password(admin_pass):
				print('Invalid password')
				admin_pass = read_option('Admin password')

			u = User(admin_name, admin_email, admin_pass, True)
			db.session.add(u)

		db.session.commit()

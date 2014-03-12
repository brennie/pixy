#!/usr/bin/env python3.3

##
# \file setup.py
# \brief Pixy administrator script
# Use this script to set up the database and add admins

'''
Pixy administrator script.

Usage:
  setup.py config
  setup.py db-create
  setup.py db-drop
  setup.py add-admin
  setup.py run-devel
  setup.py -h
 '''

from pixy import PixyApp
from pixy.models import db, User

from sqlalchemy.exc import SQLAlchemyError

import os
import stat

from docopt import docopt

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

def config():
	cfg = {}

	print('Database configuration:')

	username = read_option('Username')
	password = read_option('Password')
	hostname = read_option('Hostname')
	dbname = read_option('Database')

	cfg['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(username, password, hostname, dbname)
	cfg['SECRET_KEY'] = os.urandom(32)

	with open('pixy/pixy.cfg', 'w') as cfgFile:
		for option, value in cfg.items():
			cfgFile.write('{0}={1}\n'.format(option, repr(value)))

	os.chmod('pixy/pixy.cfg', 0o600)

def db_create():
	try:
		app = PixyApp()
		with app.app_context():
			db.create_all()
	except SQLAlchemyError as e:
		print("Could not create tables:")
		print(e)

def db_drop():
	try:
		app = PixyApp()
		with app.app_context():
			db.drop_all()
	except SQLAlchemyError as e:
		print("Could not drop tables:")
		print(e)

def add_admin():
	print('Add administrators:')

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

	try:
		app = PixyApp()
		with app.app_context():
			u = User(admin_name, admin_email, admin_pass, True)
			db.session.add(u)
			db.session.commit()
	except SQLAlchemyError as e:
		print("Could not add administrator:")
		print(e)

def run_devel():
	app = PixyApp()
	app.run()

if __name__ == '__main__':
	arguments = docopt(__doc__)
	
	if arguments['config']:
		config()
	elif arguments['db-create']:
		db_create()
	elif arguments['db-drop']:
		db_drop()
	elif arguments['add-admin']:
		add_admin()
	elif arguments['run-devel']:
		run_devel()

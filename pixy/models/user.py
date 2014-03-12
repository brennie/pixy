from flask import flash, session
from flask.ext.sqlalchemy import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

import re

from .db import db

EMAIL_RE = re.compile(r'[^@]+@[^@]+\.[^@]+')
USER_RE = re.compile(r'[a-zA-Z0-9]{2,32}')
SPECIAL_RE = re.compile(r'[^a-zA-Z0-9]')

##
# \brief A user.
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	username = db.Column(db.String(32), unique=True, nullable=False)
	email = db.Column(db.String(64), unique=True, nullable=False)
	passhash = db.Column(db.String(92), nullable=False)
	admin = db.Column(db.Boolean, nullable=False)

	##
	# \brief Create a new user model instance.
	# \param username The username.
	# \param email The email address.
	# \param password The password.
	# \param admin If the user is an admin.
	def __init__(self, username, email, password, admin=False):
		self.username = username
		self.email = email
		self.passhash = generate_password_hash(password, 'pbkdf2:sha256')
		self.admin = admin

	@staticmethod
	##
	# \brief Validate a username.
	# \param username The username to validate.
	# \return True if the username is valid and not in use; false otherwise.
	def validate_username(username):
		valid = True
		if not USER_RE.match(username):
			flash('The user name has to be an alphanumeric value between 2-32 characters', 'error')
			valid = False

		if User.query.filter_by(username=username).count() != 0:
			flash('Username already in use', 'error')
			valid = False

		return valid

	@staticmethod
	##
	# \brief Validate an email address
	# \param email The email address to validate
	# \return True if the email is valid and not in use; false otherwise.
	def validate_email(email):
		valid = True
		if not EMAIL_RE.match(email):
			flash('Invalid email', 'error')
			valid = False

		if User.query.filter_by(email=email).count() != 0:
			flash('Email already in use', 'error')
			valid = False

		if len(email) > 64:
			flash('Email must be at most 64 characters long', 'error')
			valid = False

		return valid

	@staticmethod
	##
	# \brief Validate a password
	# \param password The password to validate
	# \return True if the username is valid; false otherwise;
	def validate_password(password):
		return SPECIAL_RE.search(password) and len(password) >= 8

	@staticmethod
	##
	# \brief Validate a possible user
	# \param username The username
	# \param email The email address
	# \param password The password
	# \return True if all fields are valid; False otherwise.
	def validate_user(username, email, password, confirm):
		valid = True

		if password != confirm:
			flash('Passwords do not match', 'error')
			valid = False

		if not User.validate_username(username) or not User.validate_email(email) or not User.validate_password(password):
			valid = False

		return valid

	##
	# \brief Determine if the password given is the correct one
	# \param password The password to check
	# \return true if the password is correct; false otherwise
	def check_password(self, password):
		return check_password_hash(self.passhash, password)

	##
	# \brief Add the user entry to the session.
	def login(self):
		session['user'] = self

	##
	# \brief Remove the user entry from the session.
	def logout(self):
		delete session['user']

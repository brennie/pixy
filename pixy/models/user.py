##
# \package pixy.models.user
# \brief The package which exports the User model

from flask import flash, session
from werkzeug.security import generate_password_hash, check_password_hash

import hashlib
import re

from .db import db

##
# \brief The regex used for matching emails
EMAIL_RE = re.compile(r'[^@]+@[^@]+\.[^@]+')

##
# \brief The regex used for matching usernames
USER_RE = re.compile(r'[a-zA-Z0-9]{2,32}')

##
# \brief The regex to assert there is a special character in passwords
SPECIAL_RE = re.compile(r'[^a-zA-Z0-9]')

##
# \brief A user database model.
class User(db.Model):
	##
	# \brief The User's primary key
	id = db.Column(db.Integer, primary_key=True, nullable=False)

	##
	# \brief The User's username
	username = db.Column(db.String(32), unique=True, nullable=False)

	##
	# \brief The User's email address
	email = db.Column(db.String(64), unique=True, nullable=False)

	##
	# \brief The hash of the password
	passhash = db.Column(db.String(92), nullable=False)

	##
	# \brief A boolean flag that determines if the User is an administrator.
	admin = db.Column(db.Boolean, nullable=False)

	##
	# \brief The User's biography
	bio = db.Column(db.String(512), nullable=False)

	##
	# \brief A database relationship that links the User to all its Images.
	images = db.relationship('Image', backref='owner', lazy='dynamic')

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
                self.bio = ""


	@staticmethod
	##
	# \brief Validate a username.
	# \param username The username to validate.
	# \return True if the username is valid and not in use; false otherwise.
	def validate_username(username):
		valid = True
		if not USER_RE.match(username):
			flash('The user name has to be an alphanumeric value between 2-32 characters', 'danger')
			valid = False

		if User.query.filter_by(username=username).count() != 0:
			flash('Username already in use', 'danger')
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
			flash('Invalid email', 'danger')
			valid = False

		if User.query.filter_by(email=email).count() != 0:
			flash('Email already in use', 'danger')
			valid = False

		if len(email) > 64:
			flash('Email must be at most 64 characters long', 'danger')
			valid = False

		return valid


	@staticmethod
	##
	# \brief Validate a password
	# \param password The password to validate
	# \return True if the username is valid; false otherwise;
	def validate_password(password):
		if not SPECIAL_RE.search(password) or not len(password) >= 8:
			flash('The password must be at least 8 characters and contain a non-alphanumeric character', 'danger')
			return False

		return True

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
			flash('Passwords do not match', 'danger')
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
		session['user'] = { 'name' : self.username, 'id': self.id, 'admin': self.admin }


	@staticmethod
	##
	# \brief Remove the user entry from the session.
	def logout():
		if 'user' in session.keys():
			del session['user']


	##
	# \brief Get the gravatar URL from the user
	def get_gravatar_url(self):
		hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

		return 'http://www.gravatar.com/avatar/{0}'.format(hash)

	##
	# \brief Set the bio.
	# \param bio The new bio.
	def set_bio(self, bio):
		self.bio = bio

	##
	# \brief Set the email.
	# \param email The new email.
	def set_email(self, email):
		self.email = email

	##
	# \brief Set the password.
	# \param password The new password
	def set_password(self, password):
		self.passhash = generate_password_hash(password, 'pbkdf2:sha256')

from flask.ext.sqlalchemy import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

from .db import db

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
	def __init__(self, username, email, password, admin):
		self.username = username
		self.email = email
		self.passhash = generate_password_hash(password, 'pbkdf2:sha256')
		self.admin = admin

	##
	# \brief Determine if the password given is the correct one
	# \param password The password to check
	# \return true if the password is correct; false otherwise
	def validate(self, password):
		return check_password_hash(self.passhash, password)

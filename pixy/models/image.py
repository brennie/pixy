from flask.ext.sqlalchemy import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

import datetime
import imghdr
import os
import os.path
import tempfile

from .db import db

##
# \brief An image.
class Image(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128), nullable=False)
	private = db.Column(db.Boolean)
	owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	description = db.Column(db.String(512))
	views = db.Column(db.Integer, nullable=False)
	uploaded = db.Column(db.DateTime, nullable=False)

	ROOT = '/var/www/pixy.brennie.ca/images/' #< The root directory
	SUFFIX = '.jpg' #< The image suffix
	MAXSIZE = 1024 * 1024 #< 1 MiB

	##
	# \brief Create a new image model instance.
	# \param owner The owner.
	# \param title The title.
	# \param description The description.
	def __init__(self, owner, title, description=""):
		self.title = title
		self.owner = owner
		self.description = description
		self.views = 0
		self.uploaded = datetime.now()

	@staticmethod
	##
	# \brief Validate a image
	# \param title The image title
	# \param description The image description
	def validate(title, description, filename):
		valid = True

		if len(title > 128):
			flash('Title length must be at most 128 characters', 'error')
			valid = False

		if len(description > 512):
			flash('Description length must be at most 512 characters', 'error')
			valid = False

		if os.path.filesize(filename) > Image.MAXSIZE:
			flash('Image must be at most 1MiB', 'error')
			valid = False

		if imghdr.what(filename) != 'jpeg':
			flash('Image is not a valid JPEG image', 'error')
			valid = False

		return valid


	##
	# \brief Get the URL associated with the image.
	# \return The URL.
	def url(self):
		return 'https://pixy.brennie.ca/images/{0}.jpg'.format(self.id)

	#
	# \brief Get the path
	# \return The absolute path to the image.
	def path(self):
		return '{0}{1}{2}'.format(Image.ROOT, self.id, Image.SUFFIX)

##
# \brief A tag
class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(16), unique=True, nullable=False)

	##
	# \brief Create a new image tag model instance.
	# \param title The tag's title.
	def __init__(self, title):
		self.title = title

##
# \brief The join table between images and their tags.
imageTags = db.Table('imageTags',
	db.Column('imageID', db.Integer, db.ForeignKey('image.id')),
	db.Column('tagID', db.Integer, db.ForeignKey('tag.id'))
)

##
# \brief A table to store metadata about transforms.
class Transform(db.Model):
	id =  db.Column(db.Integer, primary_key=True)
	imageID = db.Column(db.Integer, db.ForeignKey('image.id'))
	name = db.Column(db.String(32), nullable=False)

	ROOT = '/tmp/pixy/' #< The directory for the transformed images
	PREFIX = 'transform_' #< The transform prefix
	SUFFIX = '.jpg' #< The transform suffix

	##
	# \brief Create a new transform model instance.
	def __init__(self, imageID):
		self.imageID = imageID
		self.name = tempfile.mktemp(Transform.SUFFIX, Transform.PREFIX, Transform.ROOT)

	##
	# \brief Get the path
	# \return The absolute path to the image.
	def path(self):
		return "{0}{1}{2}{3}".format(Transform.ROOT, Transform.PREFIX, self.name, Transform.SUFFIX)

	##
	# \brief Delete the file
	def unlink(self):
		os.unlink(self.path())

	##
	# \brief Save the transform.
	def save(self):
		image = Image.query.filter_by(id=self.imageID).first()
		os.rename(self.path(), image.path())

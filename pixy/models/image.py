from flask import flash, session, url_for
from flask.ext.sqlalchemy import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
import imghdr
import os
import os.path
import tempfile
import re

from .db import db
from .user import User

TAG_RE = re.compile(r'\s*([a-z]{1,16})(\s+([a-z]{1,16}))*\s*')

##
# \brief The join table between images and their tags.
imageTags = db.Table('imageTags',
	db.Column('imageID', db.Integer, db.ForeignKey('image.id')),
	db.Column('tagID', db.Integer, db.ForeignKey('tag.id'))
)

##
# \brief An image.
class Image(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128), nullable=False)
	private = db.Column(db.Boolean)
	ownerID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	description = db.Column(db.String(512))
	views = db.Column(db.Integer, nullable=False)
	uploaded = db.Column(db.DateTime, nullable=False)
	
	tags = db.relationship('Tag', secondary=imageTags, backref='images', lazy='dynamic')

	ROOT = '/var/www/pixy.brennie.ca/images/' #< The root directory
	SUFFIX = '.jpg' #< The image suffix
	MAXSIZE = 1024 * 1024 #< 1 MiB
	UPLOAD_DIR =  '/tmp/pixy/uploads'


	##
	# \brief Create a new image model instance.
	# \param owner The owner.
	# \param title The title.
	# \param description The description.
	def __init__(self, owner, private, title, description, tags):
		self.title = title
		self.ownerID = owner
		self.private = private
		self.description = description
		self.views = 0
		self.uploaded = datetime.now()
		self.set_tags(tags)


	@staticmethod
	##
	# \brief Create a temporary file
	def create_temp(file):
		filename = tempfile.mktemp(dir=Image.UPLOAD_DIR)
		file.save(filename)
		return filename


	@staticmethod
	##
	# \brief Validate a image
	# \param title The image title
	# \param description The image description
	def validate_image(title, visible, description, filename, tags):
		valid = True

		if len(title) > 128:
			flash('Title length must be at most 128 characters', 'danger')
			valid = False

		if visible not in ('public', 'private'):
			flash('Invalid value for visibility', 'danger')
			valid = False

		if len(description) > 512:
			flash('Description length must be at most 512 characters', 'danger')
			valid = False

		if os.path.getsize(filename) > Image.MAXSIZE:
			flash('Image must be at most 1MiB', 'danger')
			valid = False

		if imghdr.what(filename) != 'jpeg':
			flash('Image is not a valid JPEG image', 'danger')
			valid = False

		if not TAG_RE.match(tags):
			flash('Tags must be 1-16 alphabetic characters and seperated by spaces', 'danger')
			valid = False

		return valid


	##
	# \brief Get the URL associated with the image.
	# \return The URL.
	def url(self):
		return url_for('rawImage', id=self.id)


	##
	# \brief Get the path
	# \return The absolute path to the image.
	def path(self):
		return '{0}{1}{2}'.format(Image.ROOT, self.id, Image.SUFFIX)

	##
	# \brief Increase the view count of the image.
	def increase_view_count(self):
		self.views += 1
		db.session.commit()

	##
	# \brief Determine if the current user can edit the image
	# \return Whether or not the current user (if there is one) can edit the
	#         image.
	def editable(self):
		if 'user' not in session.keys():
			return False

		elif self.ownerID == session['user']['id']:
			return True

		elif session['user']['admin']:
			return True
		
		else:
			return False

	def viewable(self):
		if not self.private:
			return True

		elif 'user' not in session.keys():
			return False

		elif self.ownerID == session['user']['id']:
			return True

		elif session['user']['admin']:
			return True

		else:
			return False
	
	def set_title(self, title):
		self.title = title
		
	def set_description(self, description):
		self.description = description
		
	def set_tags(self, tags=None):
		if tags is None:
			self.tags = []
		else:
			imageTags = []

			for tag in set(tags.split()):
				t = Tag.query.filter_by(title=tag).first()
				if t:
					imageTags.append(t)
				else:
					imageTags.append(Tag(tag))

			self.tags = imageTags

	def set_private(self, private):
		self.private = private

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
# \brief A table to store metadata about transforms.
class Transform(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	imageID = db.Column(db.Integer, db.ForeignKey('image.id'))
	name = db.Column(db.String(32), nullable=False)

	ROOT = '/tmp/pixy/transforms/' #< The directory for the transformed images
	PREFIX = 'tr_' #< The transform prefix
	SUFFIX = '.jpg' #< The transform suffix

	##
	# \brief Create a new transform model instance.
	def __init__(self, imageID):
		self.imageID = imageID
		self.name = tempfile.mktemp(dir='') # Generate only the file name

	##
	# \brief Get the path
	# \return The absolute path to the image.
	def path(self):
		return "{0}{1}{2}{3}".format(Transform.ROOT, Transform.PREFIX, self.name, Transform.SUFFIX)

	##
	# \brief Save the transform.
	def save(self):
		image = Image.query.filter_by(id=self.imageID).first()
		os.rename(self.path(), image.path())

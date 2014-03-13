from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from .views import *
from .models import db, Image

__all__ = ('PixyApp',)

##
# \brief The actual web application instance
class PixyApp(Flask):
	##
	# \brief Create an instance of the web application
	# \param development Is the server running in development (i.e. debug) mode
	def __init__(self, development=False):
		super(PixyApp, self).__init__(__name__)

		self.config['DEBUG'] = development
		self.config['UPLOAD_FOLDER'] = Image.UPLOAD_DIR

		self.config.from_pyfile('pixy.cfg')

		db.init_app(self)

		self.add_url_rule('/', view_func=Index.as_view('index'))
		self.add_url_rule('/login', view_func=Login.as_view('login'), methods=['GET', 'POST'])
		self.add_url_rule('/logout', view_func=Logout.as_view('logout'))
		self.add_url_rule('/register', view_func=Register.as_view('register'), methods=['GET', 'POST'])
		self.add_url_rule('/profile', view_func=Profile.as_view('ownprofile'))
		self.add_url_rule('/profile/<id>', view_func=Profile.as_view('profile'))
		self.add_url_rule('/upload', view_func=Upload.as_view('upload'), methods=['GET', 'POST'])

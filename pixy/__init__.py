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

		self.add_url_rule('/', view_func=IndexView.as_view('index'))
		self.add_url_rule('/login', view_func=LoginView.as_view('login'), methods=['GET', 'POST'])
		self.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
		self.add_url_rule('/register', view_func=RegisterView.as_view('register'), methods=['GET', 'POST'])
		self.add_url_rule('/profile', view_func=ProfileView.as_view('ownProfile'))
		self.add_url_rule('/profile/edit', view_func=EditProfileView.as_view('editProfile'), methods=['GET', 'POST'])
		self.add_url_rule('/profile/<id>', view_func=ProfileView.as_view('profile'))
		self.add_url_rule('/upload', view_func=UploadView.as_view('upload'), methods=['GET', 'POST'])
		self.add_url_rule('/image/<id>.jpg', view_func=RawImageView.as_view('rawImage'))
		self.add_url_rule('/image/<id>', view_func=ImageView.as_view('image'))
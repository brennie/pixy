from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from .views import *
from .models import db

__all__ = ('PixyApp',)

##
# \brief The actual web application instance
class PixyApp(Flask):
	##
	# \brief Create an instance of the web application
	# \param development Is the server running in development (i.e. debug) mode
	def __init__(self, development=False):
		super(PixyApp, self).__init__(__name__)

		self.config['DBUEG'] = development

		self.config.from_pyfile('pixy.cfg')

		db.init_app(self)

		self.add_url_rule('/', view_func=Index.as_view('index'))
		self.add_url_rule('/register', view_func=Register.as_view('register'))

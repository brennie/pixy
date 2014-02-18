from flask import Flask

from .views import *

__all__ = ('PixyApp',)

class PixyApp(Flask):
	def __init__(self, development=False):
		super(PixyApp, self).__init__(__name__)

		self.config["DEBUG"] = development

		self.add_url_rule('/', view_func=Index.as_view('index'))
		self.add_url_rule('/register', view_func=Register.as_view('register'))

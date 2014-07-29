##
# \package pixy
# \brief The package which exports the PixyApp class

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from .views import *
from .models import db, Image

__all__ = ('PixyApp',)


##
# \brief The actual web application instance
class PixyApp(Flask):
    ##
    # \brief Create an instance of the web application.
    # \param development Tell the server whether or not to start in development
    #                    (i.e. debug) mode.
    def __init__(self, development=False):
        super(PixyApp, self).__init__(__name__)

        self.config['DEBUG'] = development
        self.config['UPLOAD_FOLDER'] = Image.UPLOAD_DIR

        self.config.from_pyfile('pixy.cfg')

        db.init_app(self)

        self.add_url_rule('/', view_func=IndexView.as_view('index'))
        self.add_url_rule('/login', view_func=LoginView.as_view('login'),
                          methods=['GET', 'POST'])
        self.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
        self.add_url_rule('/register',
                          view_func=RegisterView.as_view('register'),
                          methods=['GET', 'POST'])
        self.add_url_rule('/profile',
                          view_func=ProfileView.as_view('ownProfile'))
        self.add_url_rule('/profile/edit',
                          view_func=EditProfileView.as_view('editProfile'),
                          methods=['GET', 'POST'])
        self.add_url_rule('/profile/<int:id>',
                          view_func=ProfileView.as_view('profile'))
        self.add_url_rule('/upload', view_func=UploadView.as_view('upload'),
                          methods=['GET', 'POST'])
        self.add_url_rule('/image/<int:id>.jpg',
                          view_func=RawImageView.as_view('rawImage'))
        self.add_url_rule('/image/<int:id>',
                          view_func=ImageView.as_view('image'))
        self.add_url_rule('/image/<int:id>/edit',
                          view_func=EditImageView.as_view('editImage'),
                          methods=['GET', 'POST'])
        self.add_url_rule('/gallery',
                          view_func=GalleryView.as_view('gallery'))
        self.add_url_rule('/gallery/<int:id>',
                          view_func=GalleryView.as_view('userGallery'))
        self.add_url_rule('/transform',
                          view_func=TransformView.as_view('transform'))

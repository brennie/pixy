##
# \package pixy.views
# \brief The package which re-exports all views used in PixyApp
#
# The views re-exported are index.IndexView, register.RegisterView,
# login.LoginView, logout.LogoutView, profile.ProfileView,
# profile.EditProfileView, upload.UploadView, image.RawImageView,
# image.ImageView, image.EditImageView, gallery.GalleryView, and
# transform.TransformView.

from .index import IndexView
from .register import RegisterView
from .login import LoginView
from .logout import LogoutView
from .profile import ProfileView, EditProfileView
from .upload import UploadView
from .image import RawImageView, ImageView, EditImageView
from .gallery import GalleryView
from .transform import TransformView
##
# \package pixy.views.logout
# \brief The package which exports LogoutView

from flask import redirect, url_for
from flask.views import View

from pixy.models import User

##
# \brief Log out a user.
class LogoutView(View):
	##
	# \brief Handle an HTTP request.
	#
	# If a user is logged in, it will be logged out.
	#
	# \return A redirect to the index page.
	def dispatch_request(self):
		User.logout()

		return redirect(url_for('index'))

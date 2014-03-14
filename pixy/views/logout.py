from flask import redirect, url_for
from flask.views import View

from pixy.models import User

class LogoutView(View):
	def dispatch_request(self):
		User.logout()

		return redirect(url_for('index'))

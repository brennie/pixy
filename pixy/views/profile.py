from flask import render_template
from flask.views import View

class Profile(View):
	def dispatch_request(self):
		return render_template('profile.html')

from flask import render_template
from flask.views import View

class Register(View):
	def dispatch_request(self):
		return render_template('register.html')

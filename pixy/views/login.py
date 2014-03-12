from flask import flash, redirect, render_template
from flask.views import View

from flask.models import db, User

class Login(View):
	def dispatch_request(self):
		if request.method == 'GET':
			return self.dispatch_get()
		else:
			return self.dispatch_post()

	def dispatch_get(self):
		return render_template('login.html')

	def dispatch_post(self):
		email = request.form['email']
		password = request.form['password']

		u = User.query.filter_by(email=email).first()

		if u is not None and u.check_password(password):
			u.login()
			flash('Successfully logged in!', 'success')
			return redirect(url_for('index'))
		else:
			flash('Email/password combination invalid')
			return redirect(url_for('login'))

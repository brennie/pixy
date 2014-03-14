from flask import flash, request, redirect, render_template, session, url_for
from flask.views import View

from pixy.models import db, User

class LoginView(View):
	def dispatch_request(self):
		if 'user' in session.keys():
			return redirect(url_for('index'))
			
		if request.method == 'GET':
			return self.dispatch_get()
		else:
			return self.dispatch_post()

	def dispatch_get(self):
		return render_template('login.html', next=request.args.get('next'))

	def dispatch_post(self):
		email = request.form['email']
		password = request.form['password']

		u = User.query.filter_by(email=email).first()

		if u is not None and u.check_password(password):
			u.login()
			flash('Successfully logged in!', 'success')
			next = request.form.get('next', url_for('index'))
			return redirect(next)
		else:
			flash('Email/password combination invalid', 'danger')
			return redirect(url_for('login'))

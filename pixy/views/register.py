from flask import flash, redirect, render_template, request, url_for
from flask.views import View

from pixy.models import db, User

class Register(View):
	def dispatch_request(self):
		if request.method == 'GET':
			return self.dispatch_get()
		else:
			return self.dispatch_post()

	def dispatch_get(self):
		return render_template('register.html')

	def dispatch_post(self):
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		confirm = request.form['password_confirmation']

		if not User.validate_user(username, email, password, confirm):
			return render_template('register.html')

		user = User(username, email, password)
		db.session.add(user)
		db.session.commit()

		flash('Registration successful', 'success')

		return redirect(url_for('login'))

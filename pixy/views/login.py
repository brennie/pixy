##
# \package pixy.views.login
# \brief The package which exports LoginView

from flask import flash, request, redirect, render_template, session, url_for
from flask.views import View

from pixy.models import db, User

##
# \brief The LoginView shows the login form and handles login requests.
class LoginView(View):
	##
	# \brief Handle an HTTP request.
	#
	# This method calls LoginView.dispatch_get if the request is an HTTP GET
	# request; it passes control to LoginView.dispatch_post if it is an HTTP
	# POST request.
	#
	# \return If a user is already logged in, then a redirect to the index
	#         is returned. Otherwise it returns the result from
	#         LoginView.dispatch_get or LoginView.dispatch_post (depending on
	#         the HTTP request method).
	def dispatch_request(self):
		if 'user' in session.keys():
			return redirect(url_for('index'))
			
		if request.method == 'GET':
			return self.dispatch_get()
		else:
			return self.dispatch_post()

	##
	# \brief Handle an HTTP GET request.
	#
	# If the next URL query parameter is given, then a hidden field is inserted
	# into the login form that tells the login view where to redirect to upon a
	# successful login.
	#
	# \return The HTML page corresponding to the login form.
	def dispatch_get(self):
		return render_template('login.html', next=request.args.get('next'))

	##
	# \brief Handle an HTTP POST request.
	#
	# If the next URL query parameter is given, then a hidden field is inserted
	# into the login form that tells the login view where to redirect to upon a
	# successful login. Otherwise, it will redirect to the index.
	#
	# \return If the login is invalid, it will redirect to the login form with
	#         warnings set. Otherwise, it will redirect to the page given by
	#         the next URL query parameter or the index.
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

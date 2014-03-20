##
# \package pixy.views.register
# The package which exports RegisterView

from flask import flash, redirect, render_template, request, url_for
from flask.views import View

from pixy.models import db, User

##
# \param RegisterView shows the registration page and handles registration
# requests.
class RegisterView(View):
	##
	# \brief Handle an HTTP request.
	#
	# This method calls RegisterView.dispatch_get if the request is an HTTP GET
	# request; it passes control to RegisterView.dispatch_post if it is an HTTP
	# POST request.
	#
	# \return If a user is already logged in, then a redirect to the index
	#         is returned. Otherwise it returns the result from
	#         RegisterView.dispatch_get or RegisterView.dispatch_post (depending on
	#         the HTTP request method).
	def dispatch_request(self):
		if 'user' in session.keys():
			return redirect(url_for('ownProfile'))

		if request.method == 'GET':
			return self.dispatch_get()
		else:
			return self.dispatch_post()

	##
	# \brief Handle an HTTP GET request.
	# \return The register HTML page.
	def dispatch_get(self):
		return render_template('register.html')

	##
	# \brief Handle an HTTP POST request.
	# \return If the registration data is valid, then a redirect to the login
	#         page is returned. Otherwise, a redirect to the register page is
	#         returned.
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

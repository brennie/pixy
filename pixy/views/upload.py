##
# \package pixy.views.upload
# \brief The package which exports UploadView

from flask import flash, redirect, request, render_template, session, request, url_for
from flask.views import View

from pixy.models import db, Image, Tag

import os

from .auth import require_login

##
# \brief UploadView shows the image upload form and handles image uploads.
class UploadView(View):

	##
	# \brief Handle an HTTP request.
	#
	# This method calls UploadView.dispatch_get if the request is an HTTP GET
	# request; it passes control to UploadView.dispatch_post if it is an HTTP
	# POST request.
	#
	# \return If a user is already logged in, then a redirect to the index
	#         is returned. Otherwise it returns the result from
	#         UploadView.dispatch_get or UploadView.dispatch_post (depending on
	#         the HTTP request method).
	@require_login
	def dispatch_request(self):
		if 'user' not in session.keys():
			return redirect(url_for('index'))

		if request.method == 'GET':
			return self.dispatch_get()
		else:
			return self.dispatch_post()


	##
	# \brief Handle an HTTP GET request
	# \returns The HTML for the image upload page.
	def dispatch_get(self):
		return render_template('upload.html')


	##
	# \brief Handle an HTTP POST request.
	# \return If the image is valid and all metadata is valid, a redirect to
	#         the image's page is returned; otherwise, a redirect to the image
	#         upload page is returned.
	def dispatch_post(self):
		file = request.files['file']
		title = request.form['title']
		visible = request.form['visible']
		description = request.form['description']
		tags = request.form['tags']

		filename = Image.create_temp(file)

		if not Image.validate_image(title, visible, description, filename, tags):
			return redirect(url_for('upload'))

		uid = session['user']['id']

		i = Image(uid, visible == 'private', title, description, tags)

		db.session.add(i)
		db.session.commit()

		os.rename(filename, i.path())

		flash('Image successfully uploaded!', 'success')

		return redirect(url_for('ownProfile'))

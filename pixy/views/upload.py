from flask import flash, redirect, request, render_template, session, request, url_for
from flask.views import View

from pixy.models import db, Image, Tag

import os

from .auth import require_login

##
# \brief The upload image view
class UploadView(View):

	@require_login
	##
	# \brief Handle HTTP request
	def dispatch_request(self):
		if 'user' not in session.keys():
			return redirect(url_for('index'))

		if request.method == 'GET':
			return self.dispatch_get()
		else:
			return self.dispatch_post()


	##
	# \brief Render the upload page
	def dispatch_get(self):
		return render_template('upload.html')


	##
	# \brief Handle an upload
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

##
# \package pixy.views.image
# \brief The package which exports RawImageView, ImageView, and EditImageView

from flask import abort, flash, make_response, render_template, redirect, request, session, send_file, url_for
from flask.views import View

from pixy.models import db, Image, User, Transform

from .auth import require_login

import os


##
# \brief The RawImageView serves a JPEG image
class RawImageView(View):
	##
	# \brief Handle an HTTP request
	# \param id The id of the image.
	# \return If id does not correspond to a valid image, then a 404 error
	#         is returned. If the corresponding image is private and the user
	#         cannot view the image (i.e. the user is not an admin or is not
	#         the image owner), then a 403 error is returned. Otherwise, the
	#         raw image data is returned.
	def dispatch_request(self, id):
		i = Image.query.filter_by(id=id).first()

		if i is None:
			abort(404)

		if not i.editable():
			abort(403)

		response = make_response(send_file(i.path()))
		response.cache_control.no_cache = True
		return response

##
# \brief The ImageView displays an image and the metadata corresponding to it.
class ImageView(View):
	##
	# \brief Handle an HTTP request.
	#
	# If the image is viewable by the user, then the view count of the image is
	# updated.
	#
	# \param id The id of the image.
	# \returns If id does not correspond to a valid image, then a 404 error
	#          is returned. If the corresponding image is private and the user
	#          cannot view the image (i.e. the user is not an admin or is not
	#          the image owner), then a 403 error is returned. Otherwise the
	#          HTML page is returned. The edit and delete buttons are enabled
	#          if the viewing user is the owner or is an admin.
	def dispatch_request(self, id):
		i = Image.query.filter_by(id=id).first()
		edit = False

		if i is not None:
			if not i.editable():
				abort(403)

			i.increase_view_count()

		if i is not None:
			i.increase_view_count()


		if 'user' in session.keys():
			viewer = User.query.filter_by(id=session['user']['id']).first()
			if viewer.admin or i.ownerID == viewer.id:
				edit = True

		return render_template('image.html', image=i, edit=edit)

##
# \brief The EditImageView allows an image's metadata and actual image data to
#        be edited (via transforms).
class EditImageView(View):
	##
	# \brief Handle an HTTP request.
	#
	# This method calls EditImageView.dispatch_get if the request is an HTTP GET
	# request; it passes control to EditImageView.dispatch_post if it is an HTTP
	# POST request.
	#
	# \param id The id corresponding to the image to edit.
	# \returns The resulting response from the EditImageView.dispatch_get or
	#          EditImageView.dispatch_post methods.
	@require_login
	def dispatch_request(self, id):
		if request.method == 'GET':
			return self.dispatch_get(id)
		else:
			return self.dispatch_post(id)

	##
	# \brief Handle an HTTP GET request.
	# \param id The id of the image to edit.
	# \return If given id is invalid, then a 404 error is returned. If the image
	#         is not editable by the user, then a redirect to the index is
	#         returned. Otherwise, the edit image HTML page for the image
	#         corresponding to the given id is shown.
	def dispatch_get(self, id):
		i = Image.query.filter_by(id=id).first()

		if i is None:
			abort(404)

		if not i.editable():
			flash('You cannot edit that image', 'danger')
			return redirect(url_for('index'))

		return render_template('editImage.html', image=i)

	##
	# \brief Handle an HTTP POST request.
	# \param id The id of the image to edit.
	# \return If given id is invalid, then a 404 error is returned. If the image
	#         is not editable by the user, then a redirect to the index is
	#         returned.
	#         If the action given is 'delete', then the confirm delete page is
	#         returned. If the action is 'confirmDelete', then a redirect for
	#         the index is returned. If the action is 'edit', then a redirect
	#         for the image page is returned. Otherwise a redirect for the index
	#         is returned.
	def dispatch_post(self, id):
		action = request.form.get('action')

		i = Image.query.filter_by(id=id).first()

		if i is None:
			abort(404)

		if not i.editable():
			flash('You cannot edit that image', 'danger')
			return redirect(url_for('index'))

		if action == 'delete':
			return render_template('delete.html', image=i)

		elif action == 'confirmDelete':
			os.unlink(i.path())
			db.session.delete(i)
			db.session.commit()

			flash('Image deleted', 'success')
			return redirect(url_for('index'))

		elif action == 'edit':

			title = request.form['title']
			visible = request.form['visible']
			transform = request.form['transform']
			description = request.form['description']
			tags = request.form['tags']

			if not Image.validate_image(title, visible, description, i.path(), tags):
				return redirect(url_for('editImage', id=id))

			i.set_title(title)
			i.set_description(description)
			i.set_private(visible == 'private')
			i.set_tags(tags)

			if transform != 'none':
				tr = Transform.query.filter_by(imageID=id).first()
				if tr is not None:
					tr.save()
					db.session.delete(tr)
			
			db.session.commit()

			return redirect(url_for('image', id=id))

		else:
			return redirect(url_for('index'))


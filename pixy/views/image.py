from flask import abort, flash, make_response, render_template, redirect, request, session, send_file, url_for
from flask.views import View

from pixy.models import db, Image, User, Transform

from .auth import require_login

import os

class RawImageView(View):
	def dispatch_request(self, id):
		i = Image.query.filter_by(id=id).first()

		if i is None:
			abort(404)

		response = make_response(send_file(i.path()))
		response.cache_control.no_cache = True
		return response

class ImageView(View):
	def dispatch_request(self, id):
		i = Image.query.filter_by(id=id).first()
		edit = False

		if i is not None:
			i.increase_view_count()

		if 'user' in session.keys():
			viewer = User.query.filter_by(id=session['user']['id']).first()
			if viewer.admin or i.ownerID == viewer.id:
				edit = True

		return render_template('image.html', image=i, edit=edit)

class EditImageView(View):
	@require_login
	def dispatch_request(self, id):
		if request.method == 'GET':
			return self.dispatch_get(id)
		else:
			return self.dispatch_post(id)

	def dispatch_get(self, id):
		i = Image.query.filter_by(id=id).first()

		if i is None:
			abort(404)

		if not i.editable():
			flash('You cannot edit that image', 'danger')
			return redirect(url_for('index'))

		return render_template('editImage.html', image=i)

	def dispatch_post(self, id):
		action = request.form.get('action')

		i = Image.query.filter_by(id=id).first()

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

			if transform is not None:
				tr = Transform.query.filter_by(imageID=id).first()
				tr.save()
				db.session.delete(tr)
			
			db.session.commit()

			return redirect(url_for('image', id=id))

		else:
			return redirect(url_for('index'))


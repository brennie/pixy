from flask import abort, session, send_file, render_template
from flask.views import View

from pixy.models import Image, User

from .auth import require_login

class RawImageView(View):
	def dispatch_request(self, id):
		i = Image.query.filter_by(id=id).first()

		if i is None:
			abort(404)

		return send_file(i.path())

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

		i = Image.query.filter_by(id=id).first()

		if i is None:
			abort(404)

		if session['user']['id'] != i.ownerID and not session['user']['admin']:
			flash('You cannot edit that image', 'danger')
			return redirect(url_for('index'))

		return render_template('editImage.html', image=i) 
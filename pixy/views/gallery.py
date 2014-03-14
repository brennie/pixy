from flask import flash, redirect, request, render_template, session, url_for
from flask.views import View

from flask.ext.sqlalchemy import Pagination

from pixy.models import db, User, Image

from .auth import require_login

class GalleryView(View):
	def dispatch_request(self, id=None):
		edit = False

		images = Image.query
		user = None
		
		if id is not None:
			images = images.filter_by(ownerID=id)
			user = User.query.filter_by(id=id).first()

			if 'user' in session.keys():
				if session['user']['id'] == id:
					edit = True

				elif session['user']['admin']:
					edit = True

		elif 'user' in session.keys() and session['user']['admin']:
			edit = True

		page = int(request.args.get('page', 1))
		sort = request.args.get('sort', 'recent')

		if sort not in ('recent', 'popular'):
			sort = 'recent'

		if not edit:
			images = images.filter_by(private=False)

		if sort == 'recent':
			images = images.order_by(Image.uploaded.desc())
		else:
			images = images.order_by(Image.views.desc())

		return render_template('gallery.html',
			user=user,
			images=images.paginate(page),
			edit=edit,
			sort=sort,
			showOwner = user is None)

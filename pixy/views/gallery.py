##
# \package pixy.views.gallery
# The package which exports GalleryView

from flask import flash, redirect, request, render_template, session, url_for
from flask.views import View

from flask.ext.sqlalchemy import Pagination

from pixy.models import db, User, Image

from .auth import require_login


##
# \brief The view corresponding to the global and personal galleries
class GalleryView(View):
	##
	# \brief Handle an HTTP request
	# \param id An optional argument that determines if this is the global
	#           gallery (in which case it is equal to None) or a user-specific
	#           gallery (in which it is that user's id).
	# \return The HTML page or a redirect to the index if the id is invalid
	#         (i.e. the specified user does not exist).
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

		tag = request.args.get('tag')

		if sort not in ('recent', 'popular'):
			sort = 'recent'

		if not edit:
			images = images.filter_by(private=False)

		if tag:
			images = images.filter(Image.tags.any(title=tag))

		if sort == 'recent':
			images = images.order_by(Image.uploaded.desc())
		else:
			images = images.order_by(Image.views.desc())

		return render_template('gallery.html',
			user=user,
			images=images.paginate(page),
			edit=edit,
			sort=sort,
			tag=tag,
			showOwner = user is None)

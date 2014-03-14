from flask import flash, redirect, request, session, url_for

from functools import wraps

from pixy.models import User

def require_login(view):

	@wraps(view)
	def require_login_view(*args, **kwargs):
		if 'user' not in session.keys():
			flash('You mused be logged in to access this page.', 'danger')
			next = url_for(request.endpoint, **request.view_args)

			return redirect(url_for('login', next=next))

		return view(*args, **kwargs)

	return require_login_view
 
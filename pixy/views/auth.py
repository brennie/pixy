from flask import flash, redirect, session, url_for

from functools import wraps

from pixy.models import User

def require_login(next_view=None, **view_args):

	def require_login_view_decorator(view):

		@wraps(view)
		def require_login_view(*args, **kwargs):
			if 'user' not in session.keys():
				flash('You mused be logged in to access this page.', 'danger')
				next = url_for(next_view or request.endpoint, **view_args)

				return redirect(url_for('login', next=next))

			return view(*args, **kwargs)

		return require_login_view

	return require_login_view_decorator

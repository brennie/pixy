##
# \package pixy.views.auth
# \brief Authentication methods for PixyApp views.

from flask import flash, redirect, request, session, url_for

from functools import wraps

from pixy.models import User


##
# \brief Define a view to require a logged in user.
#
# If the user is not logged in, it will forward to the login view with a
# redirect request for the next view (stored in the next URL query parameter).
#
# \param view The view that requires a logged in user.
# \return A new view that handles the authentication.
def require_login(view):

    @wraps(view)
    def require_login_view(*args, **kwargs):
        if 'user' not in session.keys():
            flash('You mused be logged in to access this page.', 'danger')
            next = url_for(request.endpoint, **request.view_args)

            return redirect(url_for('login', next=next))

        return view(*args, **kwargs)

    return require_login_view

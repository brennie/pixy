##
# \package pixy.views.profile
# The package which exports ProfileView

from flask import flash, redirect, request, render_template, session, url_for
from flask.views import View

from pixy.models import db, User, Image

from .auth import require_login


##
# \brief The ProfileView shows a user's profile.
class ProfileView(View):
    ##
    # \brief Handle an HTTP request.
    # \param id The id of the user to whose profile we want to view. If this is
    #           None, this corresponds to a user's own profile page.
    # \return If the user is logged in and id corresponds to its id, a redirect
    #         is issued to the own profile page (where id is None). Otherwise,
    #         if the id corresponds to a user then that user's profile is
    #         returned with all viewable images. If the user does not exist, a
    #         redirect to the index is returned.
    def dispatch_request(self, id=None):
        if id is None and 'user' not in session.keys():
            return redirect('index')

        ownProfile = False
        edit = False

        if id is None:
            id = session['user']['id']
            ownProfile = True
        elif 'user' in session.keys() and id == session['user']['id']:
            return redirect(url_for('ownProfile'))

        u = User.query.filter_by(id=id).first()

        if u is None:
            return redirect(url_for('index'))

        if ownProfile:
            edit = True
        elif 'user' in session.keys():
            viewer = User.query.filter_by(id=session['user']['id']).first()
            if viewer.admin:
                edit = True

        if not ownProfile and not edit:
            recent = u.images.filter_by(private=False). \
                order_by(Image.uploaded.desc())
            popular = u.images.filter_by(private=False). \
                order_by(Image.views.desc())
        else:
            recent = u.images.order_by(Image.uploaded.desc())
            popular = u.images.order_by(Image.views.desc())

        return render_template('profile.html',
                               user=u,
                               ownProfile=ownProfile,
                               edit=edit,
                               recentCount=recent.count(),
                               popularCount=popular.count(),
                               recent=recent.limit(5),
                               popular=popular.limit(5))


##
# \brief The EditProfileView shows the form to edit a user's profile.
class EditProfileView(View):
    ##
    # \brief Handle an HTTP request
    #
    # This method calls EditProfileView.dispatch_get if the request is an HTTP
    # GET request; it passes control to EditProfileView.dispatch_post if it is
    # an HTTP POST request.
    #
    # \return If the user is not logged in, it returns a redirect to the login
    #         page. Otherwise it returns either the
    #         EditProfileView.dispatch_get (on an HTTP GET)
    #         or EditProfileView.dispatch_post (on an HTTP POST).
    @require_login
    def dispatch_request(self):
        if request.method == 'GET':
            return self.dispatch_get()
        else:
            return self.dispatch_post()

    ##
    # \brief Handle an HTTP GET request
    # \return The edit profile HTML page
    def dispatch_get(self):
        u = User.query.filter_by(id=session['user']['id']).first()
        return render_template('editProfile.html', bio=u.bio,
                               avatar=u.get_gravatar_url(), email=u.email)

    ##
    # \brief Handle an HTTP POST request
    # \return If the POSTed data is valid, it returns a redirect to the
    #         profile view. Otherwise it returns a redirect to the edit profile
    #         page with error messages.
    def dispatch_post(self):
        bio = request.form['bio']

        u = User.query.filter_by(id=session['user']['id']).first()

        if len(bio) > 512:
            flash('Bio cannot exceed 512 characters', 'danger')
        elif bio != u.bio:
            flash('Bio set successfully', 'success')
            u.set_bio(bio)

        if 'change_email' in request.form.keys():
            newEmail = request.form['email']

            if newEmail != u.email and User.validate_email(newEmail):
                flash('Email changed successfully', 'success')
                u.set_email(newEmail)

        if 'change_password' in request.form.keys():
            current = request.form['current_password']
            password = request.form['password']
            password_confirmation = request.form['password_confirmation']

            print(request.form)

            if not u.check_password(current):
                flash('You provided the wrong password', 'danger')
            elif password != password_confirmation:
                flash('The passwords do not match', 'danger')
            elif User.validate_password(password):
                flash('Password changed successfully', 'success')
                u.set_password(password)

        db.session.commit()

        return redirect(url_for('editProfile'))

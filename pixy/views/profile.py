from flask import flash, redirect, request, render_template, session, url_for
from flask.views import View

from pixy.models import db, User, Image

from .auth import require_login


class ProfileView(View):
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
			recent = Image.query.filter_by(ownerID=id, private=False).order_by(Image.uploaded.desc())
			popular = Image.query.filter_by(ownerID=id, private=False).order_by(Image.views.desc())
		else:
			recent = Image.query.filter_by(ownerID=id).order_by(Image.uploaded.desc())
			popular = Image.query.filter_by(ownerID=id).order_by(Image.views.desc())

		return render_template('profile.html',
			user = u,
			ownProfile = ownProfile,
			edit = edit,
			recentCount = recent.count(),
			popularCount = popular.count(),
			recent = recent.limit(5),
			popular = popular.limit(5))

class EditProfileView(View):
	@require_login('editProfile')
	def dispatch_request(self):
		if request.method == 'GET':
			return self.dispatch_get()
		else:
			print('dispatching post')
			return self.dispatch_post()

	def dispatch_get(self):
		u = User.query.filter_by(id=session['user']['id']).first()
		return render_template('editProfile.html', bio=u.bio, avatar=u.get_gravatar_url(), email=u.email)

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
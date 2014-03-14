from flask import redirect, request, render_template, session, url_for
from flask.views import View

from pixy.models import db, User, Image

from .auth import require_login


class ProfileView(View):
	def dispatch_request(self, id=None):
		if id is None and 'user' not in session.keys():
			return redirect('index')

		ownProfile = False

		if id is None:
			id = session['user']['id']
			ownProfile = True
		elif id == session['user']['id']:
			return redirect(url_for('profile'))

		u = User.query.filter_by(id=id).first()

		if u is None:
			return redirect(url_for('index'))

		if not ownProfile:
			recent = Image.query.filter_by(owner=id, private=False).order_by(Image.uploaded.desc())
			popular = Image.query.filter_by(owner=id, private=False).order_by(Image.views.desc())
		else:
			recent = Image.query.filter_by(owner=id).order_by(Image.uploaded.desc())
			popular = Image.query.filter_by(owner=id).order_by(Image.views.desc())

		return render_template('profile.html',
			username=u.username,
			bio=u.bio,
			gravatar_url=u.get_gravatar_url(),
			ownProfile=ownProfile,
			recentCount = recent.count(),
			popularCount = popular.count(),
			recent=recent,
			popular=popular)

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
		return render_template('editProfile.html', bio=u.bio, avatar=u.get_gravatar_url())

	def dispatch_post(self):
		print('one')
		bio = request.form['bio']
		print(list(request.form.keys()))
		#change_password = request.form['change_password']
		#change_email = request.form['change_email']
		print('two')
		valid = True
		print('three')
		if len(bio) > 512:
			flash('Bio cannot exceed 512 characters', 'danger')
			valid = False

		#return render_template('index.html')
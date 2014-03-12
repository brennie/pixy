from flask import redirect, render_template, session, url_for
from flask.views import View

from pixy.models import User

class Profile(View):
	def dispatch_request(self, id=None):
		if id is None and 'user' not in session.keys():
			return redirect('index')

		ownProfile = False

		if id is None:
			id = session['user']['id']
		elif id == session['user']['id']:
			return redirect(url_for('profile'))

		u = User.query.filter_by(id=id).first()

		if u is None:
			return redirect(url_for('index'))

		return render_template('profile.html',
			username=u.username,
			gravatar_url=u.get_gravatar_url(),
			ownProfile=ownProfile)

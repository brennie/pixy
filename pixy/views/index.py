from flask import render_template
from flask.views import View

from pixy.models import Image, User

class IndexView(View):
	def dispatch_request(self):
		recent = Image.query.filter_by(private=False).order_by(Image.uploaded.desc())
		popular = Image.query.filter_by(private=False).order_by(Image.views.desc())

		return render_template('index.html',
			recent=recent.limit(5), recentCount=recent.count(),
			popular=popular.limit(5), popularCount=popular.count(),
			showOwner=True)

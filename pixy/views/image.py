from flask import abort, send_file, render_template
from flask.views import View

from pixy.models import Image

class RawImageView(View):
	def dispatch_request(self, id):
		i = Image.query.filter_by(id=id).first()

		if i is None:
			abort(404)

		return send_file(i.path())

class ImageView(View):
	def dispatch_request(self, id):
		i = Image.query.filter_by(id=id).first()

		if i is not None:
			i.increase_view_count()

		return render_template('image.html', image=i)

class EditImageView(View):
	def dispatch_request(self, id):
		return 'edit image view'
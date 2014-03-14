from flask import abort, request, session, send_file, render_template
from flask.views import View

from pixy.models import Image, Transform, User

from .auth import require_login

import pixy.transforms

class TransformView(View):
	def dispatch_request(self):
		if 'user' not in session.keys():
			return '{"error" : "You must be logged in."}'


		id = request.args.get('id')
		transform = request.args

		return str(request.args)
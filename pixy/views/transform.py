from flask import abort, request, session, send_file, render_template
from flask.views import View

from pixy.models import db, Image, Transform, User

from .auth import require_login

import pixy.transforms

import base64

class TransformView(View):
	def dispatch_request(self):
		if 'user' not in session.keys():
			return '{"error" : "You must be logged in."}'

		transform = request.args.get('transform')
		id = request.args.get('id')

		if transform is None:
			return '{"error" : "You must specify a transform."}'
		
		im = Image.query.filter_by(id=id).first()

		if not im.editable():
			return '{"error" : "This is not your image"}'

		tr = Transform.query.filter_by(imageID=id).first()

		if tr is None:
			tr = Transform(id)
			db.session.add(tr)

		try:
			if transform == 'blur':
				radius = request.args.get('radius')
				
				if radius is None:
					return '{"error": "Require blur radius to do blur"}'
				else:
					radius = int(radius)
					if radius > 3:
						return '{"error": "Radius cannot be greater than 3"}'
					elif radius <= 0:
						return '{"error": "Radius must be at least 1"}'

				pixy.transforms.blur(im.path(), tr.path(), radius)

			elif transform == 'brightdark':
				factor = request.args.get('factor')

				if factor is None:
					return '{"error" : "Require brightdark factor to do brightdark"}'
				
				factor = int(factor)
				pixy.transforms.brightdark(im.path(), tr.path(), factor)

			elif transform == 'edges':
				pixy.transforms.edges(im.path(), tr.path())

			elif transform == 'greyscale':
				pixy.transforms.greyscale(im.path(), tr.path())

			elif transform == 'invert':
				pixy.transforms.invert(im.path(), tr.path())

			elif transform == 'pseudocolour':
				pixy.transforms.pseudocolour(im.path(), tr.path())

			elif transform == 'sepia':
				pixy.transforms.sepia(im.path(), tr.path())

			elif transform == 'sharpen':
				factor = request.args.get('factor')

				if factor is None:
					return '{"error": "Require sharpen factor to sharpen"}'
				else:
					factor = float(factor)

					if factor < 0.0:
						return '{"error": "Factor cannot be less than 0"}'
					elif factor > 10.0:
						return '{"error": "Factor cannot be greater than 10"}'

					pixy.transforms.sharpen(im.path(), tr.path(), factor)
			
			else:
				return '{"error" : "Invalid transform"}'

		except pixy.transforms.error as e:
			return '{{"error": "{0}"}}'.format(e)


		db.session.commit()
		
		imData = None
		with open(tr.path(), 'rb') as f:
			imData = f.read()

		return '{{"url": "data:image/jpeg;base64,{0}"}}'.format(base64.b64encode(imData).decode('utf-8'))

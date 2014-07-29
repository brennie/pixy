##
# \package pixy.views.index
# \brief The package which exports IndexView

from flask import render_template
from flask.views import View

from pixy.models import Image, User


##
# \brief The view corresponding to the index.
class IndexView(View):
    ##
    # \brief Handle an HTTP request.
    # \returns The HTML page with the top 5 recent and popular images.
    def dispatch_request(self):
        recent = Image.query.filter_by(private=False). \
            order_by(Image.uploaded.desc())
        popular = Image.query.filter_by(private=False). \
            order_by(Image.views.desc())

        return render_template('index.html',
                               recent=recent.limit(5),
                               recentCount=recent.count(),
                               popular=popular.limit(5),
                               popularCount=popular.count(),
                               showOwner=True)

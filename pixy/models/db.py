##
# \package pixy.models.db
# \brief The package which exports the global database object.

from flask.ext.sqlalchemy import SQLAlchemy

##
# \brief The database object.
db = SQLAlchemy()

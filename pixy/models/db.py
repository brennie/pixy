##
# \package pixy.models.db
# \brief The package which exports the global database object.

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy() #< The database object

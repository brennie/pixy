##
# \file
# \brief Export an instance of the Pixy application for the UWSGI server
#
# To run this, use:
#     uwsgi --ini pixy.ini

from pixy import PixyApp

app = PixyApp()

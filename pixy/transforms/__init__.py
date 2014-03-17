##
# \file Python 3 wrapper around the generated library so that methods have
#       correct signatures.
# \package pixy.transforms

'''Perform image transformations on JPEG images.'''

import pixy.transforms.transforms

# Re-export constants and the pixy.transforms.error class.
from .transforms import error

##
# \brief Blur an image.
#
# The blur radius should be greater than 1 but no more than 10 (soft limit); it
# can be done for arbitrarily high values of radius, but it will quite slow.
#
# \param input The input file name.
# \param output The output file name.
# \param radius The radius to blur.
def blur(input, output, radius):
    transforms.blur(input, output, radius)

##
# \brief Invert an image
# \param input The input file name.
# \param output The output file name.
def invert(input, output):
    transforms.invert(input, output)

##
# \brief Transform an image to greyscale.
# \param input The input file name.
# \param output The output file name.
def greyscale(input, output):
    transforms.greyscale(input, output)

##
# \brief Transform an image to sepia.
# \param input The input file name.
# \param output The output file name.
def sepia(input, output):
    transforms.sepia(input, output)

##
# \brief Transform an image to pseudocolour.
# \param input The input file name.
# \param output The output file name.
def pseudocolour(input, output):
    transforms.pseudocolour(input, output)

##
# \brief Brighten or darken an image.
# \param input The input file name.
# \param output The output file name.
def brightdark(input, output, factor):
    transforms.brightdark(input, output, factor)

##
# \brief Perform edge detection.
# \param input The input file name.
# \param output The output file name.
def edges(input, output):
    transforms.edges(input, output)

##
# \brief Sharpen an image
# \param input The input file name.
# \param output The output file name.
# \param factor The amount to sharpen in [0,10].
def sharpen(input, output, factor):
    transforms.sharpen(input, output, factor)

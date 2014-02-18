##
# \file Python 3 wrapper around the generated library so that methods have
#       correct signatures.
# \package pixy.transforms

"""Perform image transformations on JPEG images."""

import pixy.transforms.transforms

# Re-export constants and the pixy.transforms.error class.
from .transforms import error, FLIP_HORIZONTAL, FLIP_VERTICAL, ROTATION_QUARTER, \
                        ROTATION_HALF, ROTATION_THREE_QUARTER

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
    """Perform averaging blur on the input image and store it in output."""
    transforms.blur(input, output, radius)

##
# \brief Invert an image
# \param input The input file name.
# \param output The output file name.
def invert(input, output):
    """Invert the input image and store it in output."""
    transforms.invert(input, output)

##
# \brief Flip an image.
# \param input The input file name.
# \param output The output file name.
# \param flip The flip. This must be one of transforms.FLIP_VERTICAL or
#             transforms.FLIP_HORIZONTAL.
def flip(input, output, flip):
    """Flip the input image by the specified flip and store it in output."""
    transforms.flip(input, output, flip)

##
# \brief Rotate an image.
# \param input The input filename.
# \param output The output filename.
# \param rotation The rotation. This must be one of transforms.ROTATION_QUARTER,
#                 transforms.ROTATION_HALF, or transforms.ROTATION_THREE_QUARTER.
def rotate(input, output, rotation):
    """Rotate the input image by the specified rotation and store it in
    output.
    """
    transforms.rotate(input, output, flip)

##
# \brief Transform an image to greyscale.
# \param input The input file name
# \param output The output file name
def greyscale(input, output):
    """Transform an image to greyscale."""
    transforms.greyscale(input, output)

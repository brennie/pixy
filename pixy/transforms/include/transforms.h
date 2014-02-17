#ifndef INCLUDE_TRANSFORMS_H
#define INCLUDE_TRANSFORMS_H

#include "image.h"

/**
 * \brief Blur the given image.
 * \param image The image to blur.
 * \param radius The blur radius.
 */
void blur(Image &image, unsigned radius);

/**
 * \brief Invert the colour values of the image.
 * \param image The image to invert.
 */
void invert(Image &image);

#endif
#ifndef INCLUDE_TRANSFORMS_H
#define INCLUDE_TRANSFORMS_H

#include "image.h"

/**
 * \brief An enumeration representing a clockwise rotation.
 */
enum class Rotation
{
	Quarter = 0,     /*< Rotate by a quarter turn. */
	Half = 1,        /*< Rotate by a half turn. */
	ThreeQuarter = 2 /*< Rotate by a three-quarter turn. */
};

/**
 * \brief An enumeration representing a flip.
 */
enum class Flip
{
	Horizontal = 0, /*< Flip horizontally. */
	Vertical = 1    /*< Flip vertically. */
};

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

/**
 * \brief Flip the given image.
 * \param image The image to flip.
 * \param flip The flip.
 */
void flip(Image &image, Flip flip);

/**
 * \brief Rotate the given image.
 * \param image The image to rotate.
 * \param rotation The rotation.
 */
void rotate(Image &image, Rotation rotation);




#endif
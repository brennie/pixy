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

/**
 * \brief Convert an image to greyscale.
 * \param image The image to convert to greyscale.
 */
void greyscale(Image &image);

/**
 * \brief Convert an image to sepia.
 * \param image The image to convert to sepia.
 */
void sepia(Image &image);

/**
 * \brief Brighten or darken the given image.
 * \param image The image to brighten or darken.
 * \param factor The factor by which to brighten or darken.
 */
void brightdark(Image &image, int factor);

/**
 * \brief Convert an image to sepia.
 * \param image The image to convert to sepia.
 */
void sepia(Image &image);

/**
 * \brief Convert an image to use pseudocolour.
 * \param image The image to convert to use pseudocolour.
 */
void pseudocolour(Image &image);

/**
 * \brief Sharpen the given image.
 * \param image The image to sharpen.
 * \param factor The factor by which to sharpen the image.
 */
void sharpen(Image &image, int factor);

/**
 * \brief Make an edge image of the given image.
 * \param image The image to convert to an edge image.
 */
void edges(Image &image);

#endif

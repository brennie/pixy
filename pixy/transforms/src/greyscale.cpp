/**
 * \file
 * \brief Definition of greyscale transform
 */

#include "transforms.h"

void greyscale(Image &image)
{
	const size_t width = image.width();
	const size_t height = image.height();

	for (size_t i = 0; i < height; i++)
		for (size_t j = 0; j < width; j++)
		{
			byte avg = (image(Image::Red, i, j) + image(Image::Green, i, j) + image(Image::Blue, i, j))/3;

			image(Image::Red, i, j)	= avg;
			image(Image::Green, i, j) = avg;
			image(Image::Blue, i, j) = avg;
		}
}

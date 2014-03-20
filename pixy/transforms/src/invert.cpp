/**
 * \file
 * \brief Definition of invert transform.
 */

#include "transforms.h"

void invert(Image &image)
{
	const size_t width = image.width();
	const size_t height = image.height();

	for (size_t i = 0; i < height; i++)
		for (size_t j = 0; j < width; j++)
			for (unsigned colour = Image::Red; colour <= Image::Blue; colour++)
				image(colour, i, j) = 255 - image(colour, i, j);
}

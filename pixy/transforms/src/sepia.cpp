/**
 * \file
 * \brief Definition of sepia transform.
 */

#include <algorithm>

#include "transforms.h"

void sepia(Image &image)
{
	const size_t width = image.width();
	const size_t height = image.height();
	const unsigned max = 255;

	for (size_t i = 0; i < height; i++)
		for (size_t j = 0; j < width; j++)
		{
			unsigned red = image(Image::Red, i, j) * .393 + image(Image::Green, i, j) * 0.769 + image(Image::Blue, i, j) * 0.189;
			unsigned green = image(Image::Red, i, j) * .349 + image(Image::Green, i, j) * 0.686 + image(Image::Blue, i, j) * 0.168;
			unsigned blue = image(Image::Red, i, j) * .272 + image(Image::Green, i, j) * 0.534 + image(Image::Blue, i, j) * 0.131;

			image(Image::Red, i, j)	= static_cast<byte>(std::min(red, max));
			image(Image::Green, i, j) = static_cast<byte>(std::min(green, max));
			image(Image::Blue, i, j) = static_cast<byte>(std::min(blue, max));
		}
}

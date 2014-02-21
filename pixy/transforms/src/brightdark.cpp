#include "transforms.h"

void brightdark(Image &image, int factor)
{
	const size_t width = image.width();
	const size_t height = image.height();

	for (size_t i = 0; i < height; i++)
		for (size_t j = 0; j < width; j++)
		{
			if((image(Image::Red, i, j) + factor) > 255)
				image(Image::Red, i, j) = 255;
			else if((image(Image::Red, i, j) + factor) < 0)
				image(Image::Red, i, j) = 0;
			else
				image(Image::Red, i, j) += factor;

			if((image(Image::Green, i, j) + factor) > 255)
				image(Image::Green, i, j) = 255;
			else if((image(Image::Green, i, j) + factor) < 0)
				image(Image::Green, i, j) = 0;
			else
				image(Image::Green, i, j) += factor;

			if((image(Image::Blue, i, j) + factor) > 255)
				image(Image::Blue, i, j) = 255;
			else if((image(Image::Blue, i, j) + factor) < 0)
				image(Image::Blue, i, j) = 0;
			else
				image(Image::Blue, i, j) += factor;
		}
}
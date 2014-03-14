#include <cmath>

#include "transforms.h"

using namespace std;

void pseudocolour(Image &image)
{
	const size_t width = image.width();
	const size_t height = image.height();

	Image input(image);

	for (size_t i = 0; i < height; i++)
		for (size_t j = 0; j < width; j++)
		{
			for(unsigned colour = Image::Red; colour <= Image::Blue; colour++)
			{
				image(colour, i, j) = (unsigned char)((abs(sin(float((float(input(colour, i, j)) / 255.0f) * 2.0f * M_PI) + (float(colour)*M_PI)/6.0f)))*255);
			}
		}
}
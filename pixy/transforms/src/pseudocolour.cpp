#include "transforms.h"
#include <cmath>


using namespace std;

void pseudocolour(Image &image)
{
	float PI = 3.14159265;
	const size_t width = image.width();
	const size_t height = image.height();

	Image input(image);

	for (size_t i = 0; i < height; i++)
		for (size_t j = 0; j < width; j++)
		{
			for(unsigned colour = Image::Red; colour <= Image::Blue; colour++)
			{
				image(colour, i, j) = (unsigned char)((abs(sin(float((float(input(colour, i, j))/255.0f)*2.0f*PI) + (float(colour)*PI)/6.0f)))*255);
			}
		}
}
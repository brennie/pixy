#include "transforms.h"

void sharpen(Image &image, float factor)
{
	const size_t width = image.width();
	const size_t height = image.height();

	Image input(image);

	for (size_t i = 0; i < height; i++)
	{
		for (size_t j = 0; j < width; j++)
		{
			for(unsigned colour = Image::Red; colour <= Image::Blue; colour++) // 0->R, 1->G, 2->B
			{
				int current, n, s, e, w;

				// As long as we are not on an edge, calculate the value
				if(i > 0 && i < (height - 1) && j < (width - 1) && j > 0)
				{				
					current = input(colour, i, j);
					n		= input(colour, i-1, j);
					s		= input(colour, i+1, j);
					e		= input(colour, i, j+1);
					w		= input(colour, i, j-1);

					int value = -4*current + n + s + e + w;
			
					int result_value = int(float(current) - (factor)*(float(value))); // Truncate

					// Check the gray value is in range
					if(result_value >= 255)
						result_value = 255;
					else if(result_value <= 0)
						result_value = 0;

					image(colour, i, j) = (unsigned char)(result_value);
				}
			}
		}
	}
}

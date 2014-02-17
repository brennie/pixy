#include "image.h"

void blur(Image &image, unsigned blurRadius)
{
	const size_t width = image.width();
	const size_t height = image.height();
	Image input(image);

	for (size_t i = 0; i < width; i++)
	{
		for (size_t j = 0; j < height; j++)
		{
			for (unsigned colour = Image::Red; colour <= Image::Blue; colour++)
			{
				unsigned levelSum = 0;
				double normFactor = 0.0;

				for (size_t row = i >= blurRadius ? i - blurRadius : 0; row < i + blurRadius && row < height; row++)
					for (size_t col = j >= blurRadius ? j - blurRadius : 0; col < j + blurRadius && col < width; col++)
					{
						levelSum += input(colour, row, col);
						normFactor += 1.0;
					}

				image(colour, i, j) = levelSum / normFactor;
			}
		}
	}
}

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
				double levelSum = 0.0;
				unsigned count = 0;

				/* We take an average of the pixels in a square radius around
				 * the current pixel.
				 */
				for (size_t row = i >= blurRadius ? i - blurRadius : 0; row < i + blurRadius && row < height; row++)
					for (size_t col = j >= blurRadius ? j - blurRadius : 0; col < j + blurRadius && col < width; col++)
					{
						levelSum += input(colour, row, col);
						normFactor += 1;
					}

				image(colour, i, j) = levelSum / count;
			}
		}
	}
}

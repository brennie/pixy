#include <algorithm>

#include "transforms.h"

/**
 * \brief Flip an image horizontally.
 * \param image The image to flip.
 */
static void flipHorizontally(Image &image);

/**
 * \brief Flip an image vertically.
 * \param image The image to flip.
 */
static void flipVertically(Image &image);

void flip(Image &image, Flip flip)
{
	if (flip == Flip::Horizontal)
		flipHorizontally(image);
	else
		flipVertically(image);
}

static void flipHorizontally(Image &image)
{
	const size_t height = image.height();
	const size_t width = image.width();

	for (size_t i = 0; i < height; i++)
	{
		size_t j = 0, k = width - 1;

		for (; j < k; j++, k--)
			std::swap(image(i,j), image(i,k));
	}
}

static void flipVertically(Image &image)
{
	const size_t width = image.width();
	size_t i = 0, j = image.height() - 1;

	for (; i < j; i++, j--)
		for (size_t k = 0; k < width; k++)
			std::swap(image(i,k), image(j,k));
}

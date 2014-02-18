#include <algorithm>
#include <utility>

#include "transforms.h"

/**
 * \brief Rotate an image a quarter turn
 * \param image The image to rotate.
 */
static void rotateQuarter(Image &image);

/**
 * \brief Rotate an image a quarter turn
 * \param image The image to rotate.
 */
static void rotateHalf(Image &image);

/**
 * \brief Rotate an image a quarter turn
 * \param image The image to rotate.
 */
static void rotateThreeQuarter(Image &image);

void rotate(Image &image, Rotation rotation)
{
	switch (rotation)
	{
	case Rotation::Quarter:
		rotateQuarter(image);
		break;

	case Rotation::Half:
		rotateHalf(image);
		break;

	case Rotation::ThreeQuarter:
		rotateThreeQuarter(image);	
		break;
	}
}

static void rotateQuarter(Image &image)
{
	const size_t width = image.width();
	const size_t height = image.height();
	
	Image result(height, width);

	for (size_t i = 0; i < height; i++)
		for (size_t j = 0; j < width; j++)
			result(i, j) = image(height - j - 1, i);

	image = std::move(result);
}

static void rotateHalf(Image &image)
{
	const size_t width = image.width();

	size_t i = 0, j = image.height() - 1;
	for (; i < j; i++, j--)
	{
		size_t k = 0, l = width - 1;
		for (; k < l; k++, l--)
		{
			std::swap(image(i, k), image(j, l));
			std::swap(image(i, l), image(j, k));
		}
	}
}

static void rotateThreeQuarter(Image &image)
{
	const size_t width = image.width();
	const size_t height = image.height();
	
	Image result(height, width);

	for (size_t i = 0; i < height; i++)
		for (size_t j = 0; j < width; j++)
			result(i, j) = image(j, height - i - 1);

	image = std::move(result);
}

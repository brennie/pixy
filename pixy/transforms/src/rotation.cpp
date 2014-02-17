#include <algorithm>
#include <utility>

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

void flip(Image &image, Flip flip)
{
	if (flip == Flip::Horizontal)
		flipHorizontally(image);
	else
		flipVertically(image);
}

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

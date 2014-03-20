/**
 * \file
 * \brief The declaration of the Image class.
 */

#ifndef INCLUDE_IMAGE_H
#define INCLUDE_IMAGE_H

#include <cstddef>

/**
 * \brief A single byte.
 */
typedef unsigned char byte;

/**
 * \brief An instance of an image.
 */
class Image
{
public:
	/**
	 * \brief An individual pixel.
	 */
	struct Pixel
	{
		/**
		 * \brief The red component.
		 */
		byte red;

		/**
		 * \brief The green component.
		 */
		byte green;

		/**
		 * \brief the blue component.
		 */
		byte blue;
	};

	static constexpr unsigned Red = 0;
	static constexpr unsigned Green = 1;
	static constexpr unsigned Blue = 2;

	/**
	 * \brief Initialize a new image from a JPEG.
	 * \param fileName Path to file to load the image data.
	 * \exception std::runtime_error Thrown if the image cannot be loaded.
	 */
	Image(const char *fileName);

	/**
	 * \brief Initialize a new blank image.
	 * \param width The width of the image.
	 * \param height The height of the image.
	 */
	Image(size_t width, size_t height);

	/**
	 * \brief Initialize a new image copied from an old one.
	 * \param image The image to copy.
	 */
	Image(const Image &image);

	/**
	 * \brief Move construct an image.
	 * \param image The image to move.
	 */
	Image(Image &&image);

	/**
	 * \brief Deallocate memory associated with the image.
	 */
	~Image();

	/**
	 * \brief Copy assign an image.
	 * \param image The image to copy.
	 */
	Image & operator=(const Image &image);

	/**
	 * \brief Move assign an image.
	 * \param image The image to move.
	 */
	Image & operator=(Image &&image);

	/**
	 * \brief Free memory associated with the object.
	 *
	 * Equivalent to calling resize(0, 0);
	 */
	void clear();

	/**
	 * \brief Resize the image, losing all image data in the process.
	 *
	 * If either the width or height is zero, both will be set to zero.
	 *
	 * \param width The width of the image.
	 * \param height The height of the image.
	 */
	void resize(size_t width, size_t height);

	/**
	 * \brief Get the width.
	 */
	size_t width() const;

	/**
	 * \brief Get the height.
	 */
	size_t height() const;

	/**
	 * \brief Save the image data as a JPEG.
	 * 
	 * Images are saved with the highest quality factor.
	 *
	 * \param fileName Path to save the image data.
	 * \exception std::runtime_error Thrown if the image cannot be saved.
	 */
	void save(const char *fileName);

	/**
	 * \brief Access the pixel at the given position.
	 * \param row The row of the pixel.
	 * \param col The column of the pixel.
	 * \exception std::out_of_range Thrown if row > width() or col > height().
	 * \return A reference to the requested pixel.
	 */
	Image::Pixel& operator()(size_t row, size_t col);

	/**
	 * \brief Access the colour data of the given channel at the given position.
	 * \param channel The color channel.
	 * \param row The row of the colour value.
	 * \param col The column of the colour value.
	 * \exception std::out_of_range Thrown if channel is not one of Image::Red, Image::Blue, or Image::Green.
	 * \exception std::out_of_range Thrown if row > width() or col > height().
	 * \return A reference to the requested colour value.
	 */
	byte& operator()(unsigned channel, size_t row, size_t col);

private:
	size_t m_width; /**< The height of the image. */
	size_t m_height; /**< The width of the image. */
	Pixel **m_pixels; /**< The pixel data. */
	static constexpr unsigned quality = 100; /**< The quality to save images at. */
	static constexpr unsigned components = 3; /**< The number of components of each pixel. */
};

#endif

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
	 * \brief Deallocate memory associated with the image.
	 */
	~Image();

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
	 * \brief Get the width.
	 */
	size_t width() const;

	/**
	 * \brief Get the height.
	 */
	size_t height() const;

	/**
	 * \brief Access the pixel at the given position.
	 * \param row The row of the pixel.
	 * \param col The column of the pixel.
	 * \exception std::out_of_range Thrown if row > width() or col > height()
	 */
	Image::Pixel& operator()(size_t row, size_t col);

private:
	Pixel **m_pixels; /*< The pixel data. */
	size_t m_width; /*< The height of the image. */
	size_t m_height; /*< The width of the image. */
	static const unsigned quality = 100; /*< The quality to save images at. */
	static const unsigned components = 3; /*< The number of components of each pixel. */
};

#endif

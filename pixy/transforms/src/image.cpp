/**
 * \file
 * \brief Image class definitions.
 */

#include <stdexcept>

#include "image.h"
#include "../jpegloader/include/JPEGReader.h"
#include "../jpegloader/include/JPEGWriter.h"

Image::Image(const char *fileName) : m_width(0), m_height(0), m_pixels(nullptr)
{
	JPEGReader reader;

	reader.header(fileName);
	reader.setColorSpace(JPEG::COLOR_RGB);

	m_width = reader.width();
	m_height = reader.height();

	if (m_width > 0 && m_height > 0)
	{		
		m_pixels = new Image::Pixel *[m_height];
		for (size_t i = 0; i < m_height; i++)
			m_pixels[i] = new Image::Pixel[m_width];

		reader.load((byte **)m_pixels);
	}
}

Image::Image(size_t width, size_t height) : m_width(width), m_height(height), m_pixels(nullptr)
{
	if (m_width > 0 && m_height > 0)
	{
		m_pixels = new Image::Pixel *[m_height];
		
		for (size_t i = 0; i < m_height; i++)
		{
			m_pixels[i] = new Image::Pixel[m_width];
			for (size_t j = 0; j < m_width; j++)
				m_pixels[i][j].red = m_pixels[i][j].blue = m_pixels[i][j].green = 255;
		}
	}
	else
		m_width = m_height = 0;
}

Image::Image(const Image& image) : m_width(image.m_width), m_height(image.m_height), m_pixels(nullptr)
{
	if (m_width > 0 && m_height > 0)
	{
		m_pixels = new Image::Pixel *[m_height];

		for (size_t i = 0; i < m_height; i++)
		{
			m_pixels[i] = new Image::Pixel[m_width];
			for (size_t j = 0; j < m_width; j++)
				m_pixels[i][j] = image.m_pixels[i][j];
		}
	}
	else
		m_width = m_height = 0;
}

Image::Image(Image &&image) : m_width(image.m_width), m_height(image.m_height), m_pixels(image.m_pixels)
{
	image.m_pixels = nullptr;
	image.m_width = 0;
	image.m_height = 0;
}


Image::~Image()
{
	clear();
}

Image & Image::operator=(const Image &image)
{
	clear();

	/* We can just move assign from a copy of the image */
	*this = Image(image);

	return *this;
}

Image & Image::operator=(Image &&image)
{
	clear();
	
	m_height = image.m_height;
	m_width = image.m_width;
	m_pixels = image.m_pixels;
	
	image.m_pixels = nullptr;
	image.m_width = 0;
	image.m_height = 0;

	return *this;
}

void Image::clear()
{
	if (m_pixels != nullptr)
	{	
		for (size_t i = 0; i < m_height; i++)
			delete[] m_pixels[i];

		delete[] m_pixels;
		m_pixels = nullptr;
	}

	m_height = 0;
	m_width = 0;
}

void Image::resize(size_t width, size_t height)
{
	clear();

	/* If the area is non-zero, we can move-assign from a new image. */
	if (width > 0 && height > 0)
		*this = Image(width, height);
}


void Image::save(const char *fileName)
{
	JPEGWriter writer;
	writer.header(m_width, m_height, 3, JPEG::COLOR_RGB);
	writer.setQuality(quality);
	writer.write(fileName, (byte **)m_pixels);
}

size_t Image::height() const
{
	return m_height;
}

size_t Image::width() const
{
	return m_width;
}

Image::Pixel& Image::operator()(size_t row, size_t col)
{
	if (row >= m_height)
		throw std::out_of_range("row out of range");
	else if (col >= m_width)
		throw std::out_of_range("col out of range");

	return m_pixels[row][col];
}

byte& Image::operator()(unsigned channel, size_t row, size_t col)
{
	if (row >= m_height)
		throw std::out_of_range("row out of range");
	else if (col >= m_width)
	{
		std::cerr << "col: " << col << " width: "<< m_width << std::endl;
		throw std::out_of_range("col out of range");
	}

	switch(channel)
	{
	case Image::Red:
		return m_pixels[row][col].red;

	case Image::Green:
		return m_pixels[row][col].green;

	case Image::Blue:
		return m_pixels[row][col].blue;
	}

	throw std::out_of_range("Invalid colour channel");
}

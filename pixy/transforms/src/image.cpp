#include <algorithm>
#include <exception>

#include "image.h"
#include "../jpegloader/include/JPEGReader.h"
#include "../jpegloader/include/JPEGWriter.h"

Image::Image(const char *fileName)
{
	JPEGReader reader;

	reader.header(fileName);
	reader.setColorSpace(JPEG::COLOR_RGB);

	m_width = reader.width();
	m_height = reader.height();

	m_pixels = new Image::Pixel *[m_height];
	for (size_t i = 0; i < m_height; i++)
		m_pixels[i] = new Image::Pixel[m_width];

	reader.load((byte **)m_pixels);
}

Image::Image(size_t width, size_t height) : m_width(width), m_height(height)
{
	m_pixels = new Image::Pixel *[m_height];
	
	for (size_t i = 0; i < m_height; i++)
	{
		m_pixels[i] = new Image::Pixel[m_width];
		for (size_t j = 0; j < m_width; j++)
			m_pixels[i][j].red = m_pixels[i][j].blue = m_pixels[i][j].green = 255;
	}
}

Image::~Image()
{
	for (size_t i = 0; i < m_height; i++)
		delete[] m_pixels[i];

	delete[] m_pixels;
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
	if (row > m_height)
		throw std::out_of_range("row out of range");
	else if (col > m_width)
		throw std::out_of_range("col out of range");

	return m_pixels[row][col];
}

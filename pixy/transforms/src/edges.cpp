#include "transforms.h"
#include <cmath>

using namespace std;

void edges(Image &image)
{
	const size_t width = image.width();
	const size_t height = image.height();

	Image input(image);
	
	for (size_t i = 0; i < height; i++)
	{
		for (size_t j = 0; j < width; j++)
		{
			if(i > 0 && i < (height - 1) && j < (width - 1) && j > 0) // dont do anything with the edges
			{
				for(unsigned colour = Image::Red; colour <= Image::Blue; colour++) // 0->R, 1->G, 2->B
				{
					int nw, ne, sw, se, n, s, w, e;

					// vertical component hy
					nw = -1*input(colour, i-1, j-1);
					ne = -1*input(colour, i-1, j+1);
					n  = -2*input(colour, i-1, j); 
					s  = 2*input(colour, i+1, j); 
					se = input(colour, i+1, j+1); 
					sw = input(colour, i+1, j-1); 

					int hy = nw + ne + n + s + se + sw;
					if(hy > 255) hy = 255; // clamp
					else if(hy < 0) hy = 0;

					// horizontal component hx
					nw = -1*input(colour, i-1, j-1);
					ne = input(colour, i-1, j+1);
					w  = -2*input(colour, i, j-1); 
					e  = 2*input(colour, i, j+1); 
					se = input(colour, i+1, j+1); 
					sw = -1*input(colour, i+1, j-1); 

					int hx = nw + ne + w + e + se + sw;
					if(hx > 255) hx = 255; // clamp
					else if(hx < 0) hx = 0;

					unsigned char norm_derivative = (unsigned char)(sqrt(float(hy*hy) + float(hx*hx)));
					image(colour, i, j) = norm_derivative;
				}
			}
		}
	}
}

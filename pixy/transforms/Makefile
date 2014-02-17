SRC=src/image.cpp src/blur.cpp src/invert.cpp
OBJECTS=$(SRC:.cpp=.o)
CXXFLAGS=-Iinclude -std=c++11 -Wall

build: jpegloader/libjpegloader.a $(OBJECTS) 

jpegloader/libjpegloader.a:
	cd jpegloader; make libjpegloader.a

.PHONY: clean
clean:
	@rm -f $(OBJECTS)
	@cd jpegloader; make clean

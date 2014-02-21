SRC=src/image.cpp src/blur.cpp src/invert.cpp src/flip.cpp src/rotation.cpp src/greyscale.cpp src/sepia.cpp src/brightdark.cpp src/pseudocolour.cpp src/transforms.cpp
OBJECTS=$(SRC:.cpp=.o)
CXXFLAGS=-Iinclude -std=c++11 -Wall `pkg-config --cflags python3` -fPIC
LDFLAGS=`pkg-config --libs python3`

build: transforms.so

transforms.so: jpegloader/libjpegloader.a $(OBJECTS)
	g++ -o transforms.so -shared $(OBJECTS) jpegloader/libjpegloader.a -ljpeg $(LDFLAGS)

jpegloader/libjpegloader.a:
	cd jpegloader; make libjpegloader.a

.PHONY: clean
clean:
	@rm -f $(OBJECTS) transforms.so
	@cd jpegloader; make clean

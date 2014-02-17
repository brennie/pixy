SRC=src/image.cpp src/invert.cpp
OBJECTS=$(SRC:.cpp=.o)
CXXFLAGS=-Iinclude -std=c++11 -Wall

build: $(OBJECTS)

#invert: $(OBJECTS) jpegloader/libjpegloader.a
#	g++ -o $(TARGET) $(OBJECTS) -Ljpegloader -ljpegloader -ljpeg

jpegloader/libjpegloader.a:
	cd jpegloader; make libjpegloader.a

.PHONY: clean
clean:
	@rm -f $(OBJECTS)
	@cd jpegloader; make clean

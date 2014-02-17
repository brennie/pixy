SRC=src/JPEGReader.cpp src/JPEGWriter.cpp
OBJECTS=$(SRC:.cpp=.o)
CXXFLAGS=-Iinclude/ -ljpeg

build: jpegloader.a

jpegloader.a: $(OBJECTS)
	ar crf jpegloader.a $(OBJECTS)

.PHONY: clean
	@rm -f jpegloader.a $(OBJECTS)

SRC=src/JPEGReader.cpp src/JPEGWriter.cpp
OBJECTS=$(SRC:.cpp=.o)
CXXFLAGS=-Iinclude/ -ljpeg

build: libjpegloader.a

libjpegloader.a: $(OBJECTS)
	ar crf libjpegloader.a $(OBJECTS)

.PHONY: clean
clean:
	@rm -f libjpegloader.a $(OBJECTS)

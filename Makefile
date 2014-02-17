build: pixy/transforms/transforms.so

# We use a phony target so that we don't have to list dependancies here.
.PHONY: pixy/transforms/transforms.so
pixy/transforms/transforms.so:
	cd pixy/transforms; make transforms.so

.PHONY: clean
clean:
	cd pixy/transforms; make clean

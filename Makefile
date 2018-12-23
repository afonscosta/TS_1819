passthrough: passthrough.c
	gcc -Wall passthrough.c `pkg-config fuse3 --cflags --libs` -o passthrough


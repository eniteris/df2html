# df2html
Converts DF images to html

> ./df2html [path to image]

This program scans the image, and matches characters to the characters on the tileset sheet. The program outputs an html rendition of the image in full colour.

Theoretically the program should work with most tilesets; all you have to do is adjust lines 9-12 for the tile size and path to tileset sheet. However, the program only works with 1 bit tilesets (no alpha or graphical tiles)

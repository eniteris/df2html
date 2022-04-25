# df2html
Converts DF images to html

> ./df2html [path to image]

This script scans the image, and matches characters exactly to the characters on the tileset sheet. The program outputs an html rendition of the image in full colour.

For instance, this script converts this: ![map](https://i.imgur.com/fYxFDRi.png) to [this](http://htmlpreview.github.io/?https://github.com/eniteris/df2html/blob/master/map.html)

Theoretically the program should work with most tilesets; all you have to do is adjust lines 9-12 for the tile size and path to tileset sheet. However, the program only works with 1 bit tilesets (no alpha or graphical tiles). Swap out the font file and the css file to change display fonts.

Some extraneous code remains; drawing the grid lines isn't quite necessary, and neither is calculating the horizontal grid lines. Vertical grid lines seem to be work perfectly, given the one pixel gap between most characters, but there are probably edge cases where the vertical grid isn't detected properly.

2022.04.25: Added a "quickfort" flag, that, if set to true, spits out quickfort blueprints to the shell. Vaguely tested.

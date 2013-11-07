pixelwand-loader
================

An Image Loader for the PixelWand

A work in Progress that will allow you to upload a png file to the pixel wand and have it use that image as the
pattern displayed on the pixelwand.

The protocol is simple:

```
  client> xo
  wand> OKv1.0
  wand> D25
  client> W100
  client> [pixel data 25*100*3 bytes]
```

Current Protocol Version is 1.0

D line is the number of pixels supported by the wand

W line is the number of columns that upload will send

Pixel data is arranged in RGB per pixel (3 bytes) in column order (column = # pixels)

Future Protocol Changes in the works:
  * M Line to specify the size of the EEPROM memory
  * Interrupt the current running program to enter load mode

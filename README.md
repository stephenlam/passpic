# Overview
Command line tool to generate print-ready passport and visa photos.

The output will be PNG files to be printed as 4x6 inch photos since
those are cheapest to print. After printing, use a paper cutter to cut out
the 2x2 inch passport photos (or other size, e.g. 33x48mm for Chinese visa).

The tool will make full use of all available resolution for the best possible
print quality. Thus, it will not rescale the output to 300 ppi for printing,
but assumes your printer can handle an unlimited ppi.

# Dependencies
This tool requires Python 3+.

You will need a digital photo of your likeness that includes your entire
face and with some additional margin for cropping.

# Usage
First, create a measurements file for the photo you wish to process. See [taking measurements](#taking-measurements).

Run
```
   python3 passpic.py <image file>
```

The tool will generate a US passport photo and a Chinese visa photo. The output
will be located in a directory named `/out`.

# Supported countries
Passpic currently only supports
- US passport photos
- Chinese visa photo

# Taking measurements
A simple way to take measurements on MacOS is to view the input image in the
Preview app and draw rectangle selections.

For each image, passpic requires a corresponding measurements file
with these five parameters:

  1. X-coordinate of top-left corner of head
  2. Y-coordinate of top-left corner of head
  3. X-coordinate of bottom-right corner of head
  4. Y-coordinate of bottom-right corner of head
  5. Y-coordinate of eye center (eye level)

*Note: Do not include the ears when taking the measurements for the bounding box
around the head.*

The parameters should be integers separated by single spaces on a single line.

Example:
```
1024 1260 1424 1860 1585
```

The measurements file should be located in the same directory as the image file,
with a suffix `.txt`. For instance, the measurements file for `john.jpg` should be
`john.txt`.

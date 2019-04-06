#!/usr/bin/env python
import sys
import os
import argparse
import datetime
from PIL import Image
from PIL.ExifTags import TAGS

def main():
    extract(args.image)

def extract(imgFile):
    now = datetime.datetime.now()
    filename = os.path.basename(imgFile)
    output_filename = filename + ".txt"

    if not os.path.isfile(imgFile):
        sys.exit("%s is not an image")
    output = "Time: %d/%d/%d %d : %d : %d. Exif data found for %s:\n\n" % (now.year, now.month, now.day, now.hour, now.minute, now.second,
    filename)

    img = Image.open(imgFile)
    exif = img._getexif()
    exif_data = {}
    if exif:
        for (tag, value) in exif.items():
            decoded = TAGS.get(tag, tag)
            if type(value) is bytes:
                try:
                    exif_data[decoded] = value.decode("utf-8")
                except:
                    pass
            else:
                exif_data[decoded] = value
    else:
        sys.exit("No exif data to extract")

    for data in exif_data:
        output += "{}   :   {}\n".format(data, exif_data[data])

    writeOutput(output_filename, output)
    print "Output saved to %s" % (output_filename)

def writeOutput(filename, data):
    with open(filename, 'w') as f:
        f.write(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract exif data from image files')
    parser.add_argument('image', metavar='-i',type=str,help='Path to image file')
    args = parser.parse_args()
    main()

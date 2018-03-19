import os
import argparse
from PIL import Image


def rgb2bin(tuple, bit_per_channel):
    binstr = ""
    if (bit_per_channel < 8):
        for i in tuple:
            scale = i * (2 ** bit_per_channel - 1) // (2 ** 8 - 1)
            form = "{0:0%db}" % bit_per_channel
            binstr += form.format(scale)
    else:
        for i in tuple:
            form = "{0:0%db}" % bit_per_channel
            binstr += form.format(i)
    return binstr


def main():
    parser = argparse.ArgumentParser(description="A tool to change picture to .mif file.")
    parser.add_argument('-w', '--width', type=int, default=6, help="Bit per channel, by default 8", )
    parser.add_argument('input_file', help="Input pic file name")
    parser.add_argument('-o', '--output', help="Output file name.")
    args = parser.parse_args()

    bit_per_channel = args.width
    input_filename = args.input_file
    output_filename = args.output

    if output_filename is None:
        output_filename = os.path.basename(input_filename).split('.')[0] + ".mif"

    print("> Running with depth %d, output file name '%s'" % (bit_per_channel, output_filename))

    im = Image.open(input_filename)
    pwidth, pheight = im.size
    print("> Reading pic. Width: %d, Height: %d" % (pwidth, pheight))

    header = "-- Generated with pic2mif by florianso\n"

    mif_header = """
WIDTH=%d;
DEPTH=%d;

ADDRESS_RADIX=UNS;
DATA_RADIX=BIN;

CONTENT BEGIN
""" % (bit_per_channel * 3, pwidth * pheight)

    outf = open(output_filename, 'w')
    outf.write(header)
    outf.write(mif_header)

    count = 0
    for h in range(0, pheight):
        for w in range(0, pwidth):
            pixel = im.getpixel((w, h))
            line = "\t%d : %s;\n" % (count, rgb2bin(pixel, bit_per_channel))
            outf.write(line)
            count += 1

    outf.write("END;")

    im.close()
    outf.close()

    print("> Done!")


if __name__ == "__main__":
    main()

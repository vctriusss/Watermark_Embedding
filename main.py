import argparse
from src.Programm import *

parser = argparse.ArgumentParser(description='Watermark embedding and extraction programm\n')
parser.add_argument('-i', '--image', dest='image_file', help='Input image file')
parser.add_argument('-w', '--watermark', dest='wm_file', help='Watermark file')
parser.add_argument('-k', '--key', dest='key', help='Key file')
parser.add_argument('-C', dest='C', action='store_true', help='Embed watermark in the image')
parser.add_argument('-X', dest='X', action='store_true', help='Extract watermark')
parser.add_argument('-R', dest='R', action='store_true', help='Restore source image')
parser.add_argument('-I', '--images', dest='images_list', help='Paths for watermarked images', nargs='+')
parser.add_argument('-l', type=int, dest='l', help='Length of watermark(in hex symbols)')


def main():
    args = parser.parse_args()
    program = Programm(args)
    if args.C:
        program.embed()
    elif args.X:
        program.extract_watermark()
    elif args.R:
        program.exctract_cover()
    # ci_block = np.array([[15, 18, 19, 14], [13, 15, 16, 17], [18, 17, 14, 13], [23, 24, 25, 22]])
    # ssb = Create_Subsample_Blocks(ci_block)
    # ib = [Interpolate_Subsample_Block(ssbi) for ssbi in ssb]
    # print(*ib)


if __name__ == '__main__':
    main()

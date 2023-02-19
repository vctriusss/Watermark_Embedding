import argparse
from PIL import Image
from src.functions import *

parser = argparse.ArgumentParser(description='Watermark embedding and extracting programm\n'
                                             'WARNING: Image may be cropped from 1 to 3 pixels from each side')
parser.add_argument('-i', '--image', help='Image file to work with')
parser.add_argument('-w', '--watermark', type=argparse.FileType('r'))
parser.add_argument('-k', '--key', type=argparse.FileType('r'), help='Key file')
parser.add_argument('-C', action='store_true', help='Embed watermark (Cover the image)')
parser.add_argument('-U', action='store_true', help='Extract watermark (Uncover the image)')


def main():
    args = parser.parse_args()

    img = Image.open(args.image)
    new_shape = GetNewImageSize(img.size)
    img = img.crop((0, 0, new_shape[0], new_shape[1]))

    layers = (np.array(col) for col in img.split())
    img.close()

    for color, layer in enumerate(layers):
        ci_blocks = SplitArrayBySquareBlocks(layer, 4)


    a = 1


if __name__ == '__main__':
    main()

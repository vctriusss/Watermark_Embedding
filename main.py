import argparse
from pathlib import Path
from src.embed import *
from src.extract import *
from src.experiments import *

parser = argparse.ArgumentParser(description='Watermark embedding and extracting programm\n')
parser.add_argument('-i', '--image', help='Image file to embed in')
parser.add_argument('-w', '--watermark', type=argparse.FileType('r'))
parser.add_argument('-k', '--key', type=argparse.FileType('r'), help='Key file')
parser.add_argument('-C', action='store_true', help='Embed watermark (Cover the image)')
parser.add_argument('-U', action='store_true', help='Extract watermark (Uncover the image)')


def image_as_layers(path: str) -> np.ndarray:
    img = Image.open(path)
    layers = Image.Image.split(img)
    img.close()
    return np.array([np.array(layers[i]) for i in range(3)])


def exctract_cover(path1, path2, path3, path4):
    images = [image_as_layers(path1), image_as_layers(path2), image_as_layers(path3), image_as_layers(path4)]
    imgg = ExtractCoverImage(*images)
    Image.fromarray(imgg).save('new_image.png')
    print('Saved extracted image in file: new_image.png')


def embed(path, wm, mu):
    img_arr = image_as_layers(path)
    img1, img2, img3, img4 = Embed(img_arr, '1' * 14, '11010101001010010100101010100101010100101')
    Image.fromarray(img1).save('img1.png')
    Image.fromarray(img2).save('img2.png')
    Image.fromarray(img3).save('img3.png')
    Image.fromarray(img4).save('img4.png')


def extract_watermark(path: str, mu: str):
    img_arr = image_as_layers(path)
    wm = ExtractWatermark(img_arr, mu)
    print(wm)


def main():
    embed('lena.png', 1, 1)
    # extract_watermark('img1.png', '1' * 14)
    # args = parser.parse_args()
    # ci_block = np.array([[15, 18, 19, 14], [13, 15, 16, 17], [18, 17, 14, 13], [23, 24, 25, 22]])
    # ssb = Create_Subsample_Blocks(ci_block)
    # ib = Interpolate_Subsample_Block(ssb)


if __name__ == '__main__':
    main()

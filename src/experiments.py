from PIL import Image
import numpy as np
import math
from src.functions import image_as_layers
from src.extract import *


def PSNR(path1, path2):
    img1 = Image.open(path1)
    img2 = Image.open(path2)
    width, height = img1.size
    pixels1 = np.asarray(img1).reshape((width * height, 3))
    pixels2 = np.asarray(img2).reshape((width * height, 3))
    img1.close()
    img2.close()
    summ = 0
    for (pixel1, pixel2) in zip(pixels1, pixels2):
        r1, g1, b1 = pixel1
        r2, g2, b2 = pixel2
        y1 = 0.3 * r1 + 0.59 * g1 + 0.11 * b1
        y2 = 0.3 * r2 + 0.59 * g2 + 0.11 * b2
        summ += (y1 - y2) ** 2
    mse = summ / (width * height)
    psnr = 10 * math.log10(255 * 255 / mse)
    print('PSNR =', round(psnr), 'dB')


def SSIM(path1, path2):
    def SplitLayer_By8x8Blocks(arr: np.ndarray) -> np.ndarray:
        arr_h, arr_w = arr.shape
        blocks = np.reshape(arr, (arr_h // 8, 8, arr_w // 8, 8)).swapaxes(1, 2)
        return blocks.reshape(arr_h * arr_w // 64, 8, 8)
    
    img1 = image_as_layers(path1)
    img2 = image_as_layers(path2)

    c1, c2 = 6.5025, 58.5255

    blocks1 = [SplitLayer_By8x8Blocks(img1[i]) for i in range(3)]
    blocks2 = [SplitLayer_By8x8Blocks(img2[i]) for i in range(3)]
    res = 0
    for i in range(3):
        for b1, b2 in zip(blocks1[i], blocks2[i]):
            mu_x, mu_y = np.mean(b1), np.mean(b2)
            s_x, s_y = np.std(b1), np.std(b2)
            s_xy = np.cov(b1.flatten(), b2.flatten(), bias=True)[0][1]
            res += (2*mu_x*mu_y + c1) * (2*s_xy + c2) / (mu_x ** 2 + mu_y ** 2 + c1) / (s_x ** 2 + s_y ** 2 + c2)
    print('SSIM =', res / (3 * 4096))


def tamper_check(path1, path2, path3, path4):
    images = [image_as_layers(path1), image_as_layers(path2), image_as_layers(path3), image_as_layers(path4)]
    images[0][1][0][0] = 134
    images[1][2][32][256] = 2
    images[2][1][56][3] = 42
    imgg = ExtractCoverImage(*images)

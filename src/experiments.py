from PIL import Image
import numpy as np
import math


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

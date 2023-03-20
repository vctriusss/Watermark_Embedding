import numpy as np
from PIL import Image


def TDC(block: np.ndarray) -> str:
    center = min(block[1][1], block[1][2], block[2][1], block[2][2])
    edges = np.array(
        [block[3][3], block[3][2], block[3][1], block[3][0], block[2][0], block[1][0], 
         block[0][0], block[0][1], block[0][2], block[0][3], block[1][3], block[2][3]])
    lbp = IntToBin(int(np.bitwise_xor.reduce(edges[edges >= center])), 8)
    tdc1 = BinToInt(lbp[1]) ^ BinToInt(lbp[3]) ^ BinToInt(lbp[5]) ^ BinToInt(lbp[7])
    tdc2 = BinToInt(lbp[0]) ^ BinToInt(lbp[2]) ^ BinToInt(lbp[4]) ^ BinToInt(lbp[6])

    return str(tdc1) + str(tdc2)


def Lagrange_Interpolation(M: str, mu: str) -> np.ndarray:
    D = [[0, 0, 0, 0, 0, 0]] * 4
    if M == '':
        return np.array(D)

    a, b = BinToInt(mu[:6]), BinToInt(mu[6:])
    gamma = BinToInt(M) ^ BinToInt(mu[:11])
    for Y in range(1, 5):
        f = a * Y * Y + b * Y + gamma
        D_bin = IntToBin(f, 12)
        D[Y - 1] = [BinToInt(D_bin[i * 2: i * 2 + 2]) for i in range(6)]

    return np.array(D)


P = {1: (0, 1), 2: (0, 2),
     3: (1, 3), 4: (2, 3),
     5: (3, 2), 6: (3, 1),
     7: (2, 0), 8: (1, 0)}

X = {0: (1, 1), 1: (1, 2),
     2: (2, 1), 3: (2, 2)}

CO = {1: (0, 0), 2: (0, 3),
      3: (3, 0), 4: (3, 3)}

NearestCorner = {0: 0, 7: 0, 1: 1, 2: 1, 5: 2, 6: 2, 3: 3, 4: 3}


def IntToBin(n: int, length: int) -> str:
    return bin(n)[2:].zfill(length)


def BinToInt(n: str) -> int:
    return int(n, 2)


def SplitLayer_By4x4Blocks(arr: np.ndarray) -> np.ndarray:
    arr_h, arr_w = arr.shape
    blocks = np.reshape(arr, (arr_h // 4, 4, arr_w // 4, 4)).swapaxes(1, 2)
    return blocks.reshape(arr_h * arr_w // 16, 4, 4)


def FormLayer_From4x4Blocks(arr: np.ndarray, new_shape: tuple) -> np.ndarray:
    h, w = new_shape
    blocks = np.reshape(arr, (h // 4, w // 4, 4, 4)).swapaxes(1, 2)
    return np.reshape(blocks, new_shape)


def image_as_layers(path: str) -> np.ndarray:
    img = Image.open(path)
    layers = Image.Image.split(img)
    img.close()
    return np.array([np.array(layers[i]) for i in range(3)])


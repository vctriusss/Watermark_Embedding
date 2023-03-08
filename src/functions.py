import numpy as np
from math import floor, ceil


def SplitArrayBySquareBlocks(arr: np.ndarray, block_side: int) -> np.ndarray:
    arr_h, arr_w = arr.shape
    blocks = np.reshape(arr, (arr_h // block_side, block_side, arr_w // block_side, block_side)).swapaxes(1, 2)
    # return blocks
    return blocks.reshape(arr_h * arr_w // (block_side * block_side), block_side, block_side)


def TDC(block: np.ndarray) -> str:
    center = min(block[1][1], block[1][2], block[2][1], block[2][2])
    edges = np.array(
        [block[3][3], block[3][2], block[3][1], block[3][0], block[2][0], block[1][0], block[0][0], block[0][1],
         block[0][2], block[0][3], block[1][3], block[2][3]])
    lbp = bin(np.bitwise_xor.reduce(edges[edges >= center]))[2:].zfill(8)
    tdc1 = int(lbp[1], 2) ^ int(lbp[3], 2) ^ int(lbp[5], 2) ^ int(lbp[7], 2)
    tdc2 = int(lbp[0], 2) ^ int(lbp[2], 2) ^ int(lbp[4], 2) ^ int(lbp[6], 2)
    return str(tdc1) + str(tdc2)


def Lagrange_Interpolation(M: str, mu: str) -> np.ndarray:  # Tested && CORRECT
    a = int(mu[:6], 2)
    b = int(mu[6:], 2)
    gamma = int(M, 2) ^ int(mu[:11], 2)
    Ds = []
    for Y in range(1, 5):
        f = a * Y * Y + b * Y + gamma
        D_bin = (bin(f)[2:]).zfill(12)
        print(int(D_bin, 2))
        D = [int(D_bin[i * 2: i * 2 + 2], 2) for i in range(6)]
        Ds.append(D)
    return np.array(Ds)


def Create_Watermark_Images_From_Interpolated_Images(block: np.ndarray, D: np.ndarray) -> np.ndarray:
    new_block = block.copy()
    for v in range(6):
        val = (block[1][2] + 2 * block[2][1] + 3 * block[2][2]) % 4
        if 0 <= v <= 1:
            i, j = 0, v + 1
        elif 2 <= v <= 3:
            i, j = v - 1, 3
        else:
            i, j = 3, 6 - v
        diff = D[v - 1] - val
        new_block[i][j] = block[i][j] - block[i][j] % 4 + diff


def NearestCorner(i: int) -> int:  # Tested && CORRECT
    if i == 0 or i == 7:
        return 0
    if i == 1 or i == 2:
        return 1
    if i == 5 or i == 6:
        return 2
    return 3


def Create_Subsample_Blocks(block: np.ndarray) -> np.ndarray:  # Tested & CORRECT
    new_blocks = np.zeros((4, 2, 2), dtype=np.uint8)
    for i in range(2):
        for j in range(2):
            new_blocks[0][i][j] = block[2 * i][2 * j]
            new_blocks[1][i][j] = block[2 * i][2 * j + 1]
            new_blocks[2][i][j] = block[2 * i + 1][2 * j]
            new_blocks[3][i][j] = block[2 * i + 1][2 * j + 1]

    return new_blocks


def Interpolate_Subsample_Block(block: np.ndarray) -> np.ndarray:  # Tested & CORRECT
    new_block = np.zeros((4, 4), dtype=np.uint8)

    co1 = block[0][0]
    co2 = block[0][1]
    co3 = block[1][0]
    co4 = block[1][1]
    corners = [co1, co2, co3, co4]

    ad = (3 * min(corners) + 2 * max(corners)) / 5
    params = [(co1 + co2) / 2, (co2 + co4) / 2, (co3 + co4) / 2, (co1 + co3) / 2]

    edges = [0] * 8
    for i in range(8):
        val = (ad + params[i // 2]) / 2
        edges[i] = floor(val) if ad > corners[NearestCorner(i)] else ceil(val)

    new_block[1][1] = round((edges[0] + edges[7] + co1) / 3)
    new_block[1][2] = round((edges[1] + edges[2] + co2) / 3)
    new_block[2][2] = round((edges[3] + edges[4] + co4) / 3)
    new_block[2][1] = round((edges[5] + edges[6] + co3) / 3)

    new_block[0][0] = co1
    new_block[0][3] = co2
    new_block[3][0] = co3
    new_block[3][3] = co4

    new_block[0][1] = edges[0]
    new_block[0][2] = edges[1]
    new_block[1][3] = edges[2]
    new_block[2][3] = edges[3]
    new_block[3][2] = edges[4]
    new_block[3][1] = edges[5]
    new_block[2][0] = edges[6]
    new_block[1][0] = edges[7]

    return new_block

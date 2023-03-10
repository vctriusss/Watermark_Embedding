import numpy as np
from math import floor, ceil
from src.helping_functions import *


def SplitArrayBySquareBlocks(arr: np.ndarray, block_side: int) -> np.ndarray:
    arr_h, arr_w = arr.shape
    blocks = np.reshape(arr, (arr_h // block_side, block_side, arr_w // block_side, block_side)).swapaxes(1, 2)
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
    assert len(mu) == 14 and len(M) == 11
    a = int(mu[:6], 2)
    b = int(mu[6:], 2)
    gamma = int(M, 2) ^ int(mu[:11], 2)
    D = [[]] * 4
    for Y in range(1, 5):
        f = a * Y * Y + b * Y + gamma
        D_bin = (bin(f)[2:]).zfill(12)
        D[Y - 1] = [int(D_bin[i * 2: i * 2 + 2], 2) for i in range(6)]

    return np.array(D)


def Create_Watermark_Images_From_Interpolated_Images(blocks: np.ndarray, Ds: np.ndarray, AC: str) -> np.ndarray:
    new_blocks = blocks.copy()
    for bi in range(4):
        for v in range(1, 7):
            val = (new_blocks[bi][1][2] + 2 * new_blocks[bi][2][1] + 3 * new_blocks[bi][2][2]) & 3
            diff = Ds[bi][v - 1] - val

            # Edge
            pi, pj = P(v)
            new_3rd_bit = (1 if diff > 0 else (0 if diff <= 0 else new_blocks[bi][pi][pj] & 4))
            new_blocks[bi][pi][pj] = ((new_blocks[bi][pi][pj] >> 3) << 3) + 4 * new_3rd_bit + abs(diff)

            # Center
            xi, xj = X(abs(diff))
            new_blocks[bi][xi][xj] += (1 if diff > 0 else (0 if diff == 0 else -1))

        # AC & TDC
        new_blocks[bi][2][0] = ((new_blocks[bi][2][0] >> 2) << 2) + int(AC, 2)
        new_blocks[bi][1][0] = ((new_blocks[bi][1][0] >> 2) << 2) + int(TDC(blocks[bi]), 2)

        # Increase CO_u
        new_blocks[bi][(bi // 2) * 3][3 * (1 <= bi <= 2)] += 1

    return new_blocks


def ExtractDataBitsFromImageBlock(block: np.ndarray):

#     coi, coj = CO(bi + 1)
#     new_blocks[bi][coi][coj] -= 1

    Di = []
    for v in range(6, 0, -1):
        Di.append((block[1][2] + 2 * block[2][1] + 3 * block[2][2]) % 4)
        pi, pj = P(v)
        sign = block[pi][pj] & 4
        pos = block[pi][pj] % 4
        if pos:
            xi, xj = X(pos)
            block[xi][xj] += (1 if sign == 0 else -1)
    return Di


def Extract(blocks: np.ndarray, mu: str):
    a = int(mu[:6], 2)
    b = int(mu[6:], 2)

    new_blocks = blocks.copy()
    Ds = []
    for bi in range(4):
        coi, coj = CO(bi + 1)
        new_blocks[bi][coi][coj] -= 1
        D = []
        for v in range(6, 0, -1):
            D.append((new_blocks[bi][1][2] + 2 * new_blocks[bi][2][1] + 3 * new_blocks[bi][2][2]) % 4)
            pi, pj = P(v)
            sign = new_blocks[bi][pi][pj] & 4
            pos = new_blocks[bi][pi][pj] % 4
            if pos:
                xi, xj = X(pos)
                new_blocks[bi][xi][xj] += (1 if sign == 0 else -1)
        Ds.append(D[::-1])

    gammas = [np.polyval(Ds[i - 1], 4) - a * i * i - b * i for i in range(1, 5)]
    print(gammas)


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

    # Corners
    co1 = block[0][0]
    co2 = block[0][1]
    co3 = block[1][0]
    co4 = block[1][1]

    new_block[0][0] = co1
    new_block[0][3] = co2
    new_block[3][0] = co3
    new_block[3][3] = co4

    corners = [co1, co2, co3, co4]

    ad = (3 * min(corners) + 2 * max(corners)) / 5
    params = [(co1 + co2) / 2, (co2 + co4) / 2, (co3 + co4) / 2, (co1 + co3) / 2]

    # Edges
    edges = [0] * 8
    for i in range(8):
        val = (ad + params[i // 2]) / 2
        edges[i] = floor(val) if ad > corners[NearestCorner(i)] else ceil(val)
        pi, pj = P(i + 1)
        new_block[pi][pj] = edges[i]

    # Centers
    new_block[1][1] = round((edges[0] + edges[7] + co1) / 3)
    new_block[1][2] = round((edges[1] + edges[2] + co2) / 3)
    new_block[2][2] = round((edges[3] + edges[4] + co4) / 3)
    new_block[2][1] = round((edges[5] + edges[6] + co3) / 3)

    return new_block

import numpy as np
from math import floor, ceil


def SplitArrayBySquareBlocks(arr: np.ndarray, block_side: int) -> np.ndarray:
    arr_h, arr_w = arr.shape
    blocks = np.reshape(arr, (arr_h // block_side, block_side, arr_w // block_side, block_side)).swapaxes(1, 2)
    # return blocks
    return blocks.reshape(arr_h * arr_w // (block_side * block_side), block_side, block_side)


def GetNewImageSize(shape: tuple) -> tuple[int, int]:
    h, w = shape
    return h - h % 4, w - w % 4


def NearestCorner(i: int) -> int:
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

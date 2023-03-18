from math import floor, ceil
from src.functions import *


def Create_Subsample_Blocks(block: np.ndarray) -> np.ndarray:
    new_blocks = np.zeros((4, 2, 2), dtype=np.uint8)
    for i in range(2):
        for j in range(2):
            new_blocks[0][i][j] = block[2 * i][2 * j]
            new_blocks[1][i][j] = block[2 * i][2 * j + 1]
            new_blocks[2][i][j] = block[2 * i + 1][2 * j]
            new_blocks[3][i][j] = block[2 * i + 1][2 * j + 1]

    return new_blocks


def Interpolate_Subsample_Block(block: np.ndarray) -> np.ndarray:
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
    params = [co1 / 2 + co2 / 2, co2 / 2 + co4 / 2, co3 / 2 + co4 / 2, co1 / 2 + co3 / 2]

    # Edges
    edges = [0] * 8
    for i in range(8):
        val = (ad + params[i // 2]) / 2
        edges[i] = floor(val) if ad > corners[NearestCorner[i]] else ceil(val)
        pi, pj = P[i + 1]
        new_block[pi][pj] = edges[i]

    # Centers
    new_block[1][1] = round((edges[0] + edges[7] + co1) / 3)
    new_block[1][2] = round((edges[1] + edges[2] + co2) / 3)
    new_block[2][2] = round((edges[3] + edges[4] + co4) / 3)
    new_block[2][1] = round((edges[5] + edges[6] + co3) / 3)

    return new_block


def EmbedWatermarkInBlock(block: np.ndarray, D: np.ndarray, bi: int, tdc: str) -> np.ndarray:
    # TDC & Sequence number
    block[1][0] += BinToInt(tdc) - block[1][0] % 4
    block[2][0] += bi - block[2][0] % 4

    if D.size == 0:
        return block

    for v in range(1, 7):
        val = (block[1][2] + 2 * block[2][1] + 3 * block[2][2]) % 4
        diff = D[v - 1] - val

        # Edge
        pi, pj = P[v]
        new_3rd_bit = diff > 0
        block[pi][pj] += 4 * new_3rd_bit + abs(diff) - block[pi][pj] % 8

        # Center
        xi, xj = X[abs(diff)]
        block[xi][xj] += (1 if diff > 0 else (0 if diff == 0 else -1))

    return block


def EmbedInColorComponent(layer: np.ndarray, M: str, mu: str):
    shape = layer.shape
    blarr_shape = shape[0] * shape[1] // 16, 4, 4
    ci_blocks = SplitLayer_By4x4Blocks(layer)
    WM1 = np.zeros(blarr_shape, dtype=np.uint8)
    WM2 = np.zeros(blarr_shape, dtype=np.uint8)
    WM3 = np.zeros(blarr_shape, dtype=np.uint8)
    WM4 = np.zeros(blarr_shape, dtype=np.uint8)

    for i, ci_block in enumerate(ci_blocks):
        M_block = M[11 * i: 11 * (i + 1)]
        tdc = TDC(ci_block)
        subsample_blocks = Create_Subsample_Blocks(ci_block)
        ISI1 = Interpolate_Subsample_Block(subsample_blocks[0])
        ISI2 = Interpolate_Subsample_Block(subsample_blocks[1])
        ISI3 = Interpolate_Subsample_Block(subsample_blocks[2])
        ISI4 = Interpolate_Subsample_Block(subsample_blocks[3])

        Ds = Lagrange_Interpolation(M_block, mu)
        WM1[i] = EmbedWatermarkInBlock(ISI1, Ds[0], 0, tdc)
        WM2[i] = EmbedWatermarkInBlock(ISI2, Ds[1], 1, tdc)
        WM3[i] = EmbedWatermarkInBlock(ISI3, Ds[2], 2, tdc)
        WM4[i] = EmbedWatermarkInBlock(ISI4, Ds[3], 3, tdc)

    layer1 = FormLayer_From4x4Blocks(WM1, shape)
    layer2 = FormLayer_From4x4Blocks(WM2, shape)
    layer3 = FormLayer_From4x4Blocks(WM3, shape)
    layer4 = FormLayer_From4x4Blocks(WM4, shape)

    return layer1, layer2, layer3, layer4


def Embed(img: np.ndarray, mu: str, M: str):
    M = M + '0' * ((11 - len(M) % 11) % 11)

    r_layers = EmbedInColorComponent(img[0], M, mu)
    g_layers = EmbedInColorComponent(img[1], M, mu)
    b_layers = EmbedInColorComponent(img[2], M, mu)

    img1 = np.dstack((r_layers[0], g_layers[0], b_layers[0]))
    img2 = np.dstack((r_layers[1], g_layers[1], b_layers[1]))
    img3 = np.dstack((r_layers[2], g_layers[2], b_layers[2]))
    img4 = np.dstack((r_layers[3], g_layers[3], b_layers[3]))

    return img1, img2, img3, img4

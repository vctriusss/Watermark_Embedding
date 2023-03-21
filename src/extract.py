from io import StringIO
from src.functions import *


def ExtractDataBitsFromImageBlock(block: np.ndarray, a: int, b: int, mu_int11: int):
    Di = []
    for v in range(6, 0, -1):
        pi, pj = P[v]
        sign = (block[pi][pj] & 4) // 4
        diff = block[pi][pj] % 4

        xi, xj = X[diff]
        block[xi][xj] += (-1 if sign == 1 else (0 if diff == 0 else 1))

        diff = diff if sign == 1 else -diff

        Di.append((block[1][2] + 2 * block[2][1] + 3 * block[2][2]) % 4 + diff)

    Di.reverse()

    Yp = (block[2][0] % 4) + 1
    f = BinToInt(''.join(IntToBin(d, 2) for d in Di))

    new_gamma = f - a * Yp * Yp - b * Yp

    # Return Watermark
    return IntToBin(new_gamma ^ mu_int11, 11)


def ExtractCoverImageFrom4Blocks(b1: np.ndarray, b2: np.ndarray, b3: np.ndarray, b4: np.ndarray):
    new_block = np.zeros((4, 4), dtype=np.uint8)
    for i in range(2):
        for j in range(2):
            new_block[2 * i][2 * j] = b1[3 * i][3 * j]
            new_block[2 * i][2 * j + 1] = b2[3 * i][3 * j]
            new_block[2 * i + 1][2 * j] = b3[3 * i][3 * j]
            new_block[2 * i + 1][2 * j + 1] = b4[3 * i][3 * j]

    return new_block


def ExctractCoverImageLayer(img1, img2, img3, img4):
    shape = img1.shape
    img1 = SplitLayer_By4x4Blocks(img1)
    img2 = SplitLayer_By4x4Blocks(img2)
    img3 = SplitLayer_By4x4Blocks(img3)
    img4 = SplitLayer_By4x4Blocks(img4)
    ci = []
    for i in range(shape[0] * shape[1] // 16):
        ci_block = ExtractCoverImageFrom4Blocks(img1[i], img2[i], img3[i], img4[i])
        ci.append(ci_block)
        rtdc = TDC(ci_block)
        etdcs = [ExtractTDC(img1[i]), ExtractTDC(img2[i]), ExtractTDC(img3[i]), ExtractTDC(img4[i])]
        if not (rtdc == etdcs[0] == etdcs[1] == etdcs[2] == etdcs[3]):
            print(f'WARNING!!! Tamper Detected in block {i}')

    return FormLayer_From4x4Blocks(np.array(ci), shape)


def ExtractCoverImage(img1, img2, img3, img4):
    cir = ExctractCoverImageLayer(img1[0], img2[0], img3[0], img4[0])
    cig = ExctractCoverImageLayer(img1[1], img2[1], img3[1], img4[1])
    cib = ExctractCoverImageLayer(img1[2], img2[2], img3[2], img4[2])

    return np.dstack((cir, cig, cib))


def ExtractWatermark(img: np.ndarray, mu: str) -> str:
    a = BinToInt(mu[:6])
    b = BinToInt(mu[6:])
    wm = StringIO()
    lr, lg, lb = SplitLayer_By4x4Blocks(img[0]), SplitLayer_By4x4Blocks(img[1]), SplitLayer_By4x4Blocks(img[2])
    for block in lr:
        wm_part = ExtractDataBitsFromImageBlock(block, a, b, BinToInt(mu[:11]))
        wm.write(wm_part)

    return wm.getvalue().rstrip('0')


def ExtractTDC(block: np.ndarray) -> str:
    return IntToBin(block[1][0] % 4, 2)

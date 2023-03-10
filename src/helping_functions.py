def P(v: int) -> tuple[int, int]:
    assert 1 <= v <= 8
    if 1 <= v <= 2:
        return 0, v
    elif 3 <= v <= 4:
        return v - 2, 3
    elif 5 <= v <= 6:
        return 3, 7 - v
    return 9 - v, 0


def X(w: int) -> tuple[int, int]:
    assert 0 <= w <= 3
    if w < 2:
        return 1, w + 1
    return 2, w - 1


def CO(i: int) -> tuple[int, int]:
    assert 1 <= i <= 4
    if i < 3:
        return 0, (i - 1) * 3
    return 3, (i - 3) * 3


def NearestCorner(i: int) -> int:
    assert 0 <= i <= 7
    if i == 0 or i == 7:
        return 0
    if i == 1 or i == 2:
        return 1
    if i == 5 or i == 6:
        return 2
    return 3

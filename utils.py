def get_subsets(mask: int):
    s = mask
    while s > 0:
        if s != mask:
            yield s
        s = (s-1) & mask
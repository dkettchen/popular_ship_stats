def invert_rank(num:int):
    """
    takes a number <= 100

    returns the inverted percent (ie 1 -> 99, 40 -> 60, etc)
    """
    if num > 100:
        return 0
    new_num = 100-num
    return new_num

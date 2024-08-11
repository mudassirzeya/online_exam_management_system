from random import randint


def random_with_N_digits():
    range_start = 10**(8-1)
    range_end = (10**8)-1
    return randint(range_start, range_end)

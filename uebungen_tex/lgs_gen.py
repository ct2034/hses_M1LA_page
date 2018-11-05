import numpy as np
from itertools import enumerate

SIZEA = 4
SIZEB = 4

def rand_nice_numbers(a, b=1):
    return np.round(np.random.rand(a, b) * 10 - 5)

def goal_check(A, x):
    b = np.dot(A, x.T)
    if(
        (np.max(b) <= 3)
        & (np.min(b) >= 0)
    ):
        return b
    else:
        return np.array([])

def make_tex(A, x, b):
    tex = ""
    for l, il in enumerate(A):
        for c, ic in enumerate(A):


if __name__ == "__main__":
    b = np.array([])
    while not b.any():
        A = rand_nice_numbers(SIZEA, SIZEB)
        x = rand_nice_numbers(1, SIZEB)
        b = goal_check(A, x)
    print(A)
    print(x)
    print(b)

import numpy as np

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
    """
    e.g.:
    -3x_1 &  +x_2 & -3x_3 & = & -2 \\
    -4x_1 & +2x_2 & -4x_3 & = & -2 \\
     3x_1 &  -x_2 &  +x_3 & = & -2
     """
    tex = ""
    for il, l in enumerate(A):
        if len(tex):
            tex += "\\\\\n"
        for ic, c in enumerate(l):
            tex += "{0}x_{1} & ".format(int(c), int(ic)) if c != 0 else " & "
        tex += "= {0}".format(int(b[il][0]))
    tex += "\n% lsg: ("
    for n in x[0]:
        tex += "{0}, ".format(int(n))
    tex += ")"
    return tex

if __name__ == "__main__":
    b = np.array([])
    while not b.any():
        A = rand_nice_numbers(SIZEA, SIZEB)
        x = rand_nice_numbers(1, SIZEB)
        b = goal_check(A, x)
    print(make_tex(A, x, b))

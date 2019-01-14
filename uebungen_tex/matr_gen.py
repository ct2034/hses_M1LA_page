import random

import numpy as np
import pylatex

class Enumerate(pylatex.base_classes.Environment):
    """A class to wrap LaTeX's enumerate environment."""

    packages = [pylatex.Package('enumitem')]
    escape = False
    content_separator = "\n"

class Array(pylatex.base_classes.Environment):
    """A class to wrap LaTeX's array environment."""

    packages = []
    escape = False
    content_separator = "\n"

def rand_nice_numbers(a, b=1):
    return np.round(np.random.rand(a, b) * 11 - 5)

def goal_check(A, B, misproportion_possible=False):
    try:
        res = np.dot(A, B)
        if(
            (np.max(res) <= 10)
            & (np.min(res) >= -10)
            & (np.count_nonzero(res == 0) <= 1)
        ):
            return res
        else:
            return np.array([])
    except Exception as e:
        if misproportion_possible:
            return np.array([[0]])
        else:
            raise e

def make_matr_tex(A):
    tex = ""
    tex += '\\begin{bmatrix}'
    for il, l in enumerate(A):
        if il > 0:
            tex += " \\\\\n"
        for ic, c in enumerate(l):
            if ic > 0:
                tex += "& "
            tex += "{0} ".format(int(c))
    tex += '\end{bmatrix}'
    return tex

def make_tex(A, B):
    tex = ""
    for mat in [A, B]:
        if len(tex):
            tex += "\\cdot"
        tex += make_matr_tex(mat)
    return pylatex.NoEscape(tex)

def get_a_matr(m, pin, n, misproportion_possible=False):
    res = np.array([])
    while not len(res):
        A = rand_nice_numbers(m, pin)
        if misproportion_possible:
            p = pin + round(random.random() - .3)
        else:
            p = pin
        B = rand_nice_numbers(p, n)
        # print([m, pin, p, n])
        res = goal_check(A, B, misproportion_possible)
        # print(res.shape)
    return make_tex(A, B), res

def append_a_matr(doc, lsgen, m=0, p=0, n=0, misproportion_possible=False):
    doc.append(pylatex.Command('item'))
    doc.append(pylatex.Command('('))
    doc.append(pylatex.Command('displaystyle'))
    with doc.create(Array(options="t", arguments="rrrrrr")):
        if misproportion_possible:
            [m, p, n] = [random.randint(2, 3) for _ in range(3)]
        ue, lsg = get_a_matr(m, p, n, misproportion_possible)
        doc.append(ue)
        lsgen.append(lsg)
    doc.append(pylatex.Command(')'))

def append_a_det(doc, lsgen, m=0, n=0, misproportion_possible=False):
    doc.append(pylatex.Command('item'))
    doc.append(pylatex.Command('('))
    doc.append(pylatex.Command('displaystyle'))
    with doc.create(Array(options="t", arguments="rrrrrr")):
        if misproportion_possible:
            [m, n] = [random.randint(2, 3, 4) for _ in range(2)]
        A = rand_nice_numbers(m, n)
        doc.append(pylatex.NoEscape(make_matr_tex(A)))
        lsgen.append(np.linalg.det(A))
    doc.append(pylatex.Command(')'))

def append_a_lsg(doc, lsg):
    doc.append(pylatex.Command('item'))
    doc.append(pylatex.Command('('))
    doc.append(pylatex.Command('displaystyle'))
    if lsg.__class__ == np.float64:
        doc.append(str(int(round(lsg))))
    elif lsg.__class__ == np.ndarray:
        if (lsg == np.array([[0]])).all():
            doc.append("Keine Lösung")
        else:
            with doc.create(Array(options="t", arguments="rrrrrr")):
                doc.append(pylatex.NoEscape(make_matr_tex(lsg)))
    doc.append(pylatex.Command(')'))


if __name__ == "__main__":
    np.random.seed(10)
    doc_ue = pylatex.Document('matr_ue', documentclass='article', document_options='a4paper')
    doc_lsg = pylatex.Document('matr_lsg', documentclass='article', document_options='a4paper')

    doc_ue.preamble.append(pylatex.Command('title', 'Mathe 1 LA Matritzen - Übungen'))
    doc_lsg.preamble.append(pylatex.Command('title', 'Mathe 1 LA Matritzen - Lösungen'))
    for d in [doc_ue, doc_lsg]:
        d.preamble.append(pylatex.Command('author', 'Christian Henkel'))
        d.preamble.append(pylatex.Command('usepackage', 'amsfonts'))
        d.preamble.append(pylatex.Command('usepackage', 'amsmath'))
        d.preamble.append(pylatex.Command('date', pylatex.NoEscape(r'\today')))
        d.append(pylatex.Command('maketitle'))
    sec = 'Matrixmultiplikation'
    with doc_ue.create(pylatex.Section(sec)):
        doc_ue.append("Berechnen Sie die Multiplikation der folgenden Matritzen")
        lsgen_mult = []
        with doc_ue.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
            for _ in range(4):
                append_a_matr(doc_ue, lsgen_mult, 2, 2, 2)
            for _ in range(4):
                append_a_matr(doc_ue, lsgen_mult, 1, 3, 1)
            for _ in range(4):
                append_a_matr(doc_ue, lsgen_mult, 3, 3, 2)
            for _ in range(4):
                append_a_matr(doc_ue, lsgen_mult, 2, 2, 3)
            for _ in range(8):
                append_a_matr(doc_ue, lsgen_mult, misproportion_possible=True)
    # LÖSUNG
    with doc_lsg.create(pylatex.Section(sec)):
        with doc_lsg.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
            for l in lsgen_mult:
                append_a_lsg(doc_lsg, l)
    sec = 'Determinante'
    with doc_ue.create(pylatex.Section(sec)):
        doc_ue.append("Berechnen Sie die Determinante der folgenden Matritzen")
        lsgen_det = []
        with doc_ue.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
            for _ in range(4):
                append_a_det(doc_ue, lsgen_det, 2, 2)
            for _ in range(8):
                append_a_det(doc_ue, lsgen_det, 3, 3)
            for _ in range(4):
                append_a_det(doc_ue, lsgen_det, 4, 4)
            for _ in range(2):
                append_a_det(doc_ue, lsgen_det, 5, 5)
    # LÖSUNG
    # print(lsgen_det)
    with doc_lsg.create(pylatex.Section(sec)):
        with doc_lsg.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
            for l in lsgen_det:
                append_a_lsg(doc_lsg, l)

    for d in [doc_ue, doc_lsg]:
        d.generate_pdf()

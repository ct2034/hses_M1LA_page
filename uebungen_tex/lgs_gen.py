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
    return np.round(np.random.rand(a, b) * 10 - 5)

def goal_check(A, x):
    b = np.dot(A, x.T)
    if(
        (np.max(b) <= 2)
        & (np.min(b) >= -2)
        & (np.count_nonzero(A == 0) <= 1)
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
            tex += " \\\\\n"
        for ic, c in enumerate(l):
            if ic == 0:
                fstr = "{0}x_{1}&"
            else:
                fstr = "~{0:+d}x_{1}&"
            tex += fstr.format(int(c), int(ic)) if c != 0 else "~&"
        tex += "=&{0}".format(int(b[il][0]))
    return tex

def get_an_lgs(eqns, vars):
    b = np.array([])
    while not b.any():
        A = rand_nice_numbers(eqns, vars)
        x = rand_nice_numbers(1, vars)
        b = goal_check(A, x)
    return make_tex(A, x, b), x[0]

def append_an_lgs(doc, lsgen, eqns, vars):
    doc.append(pylatex.Command('item'))
    doc.append(pylatex.Command('('))
    doc.append(pylatex.Command('displaystyle'))
    with doc.create(Array(options="t", arguments="rrrrrr")):
        ue, lsg = get_an_lgs(eqns, vars)
        doc.append(ue)
        lsgen.append(lsg)
    doc.append(pylatex.Command(')'))

def append_an_lsg(doc, lsg):
    doc.append(pylatex.Command('item'))
    doc.append(pylatex.Command('('))
    doc.append(pylatex.Command('displaystyle'))
    doc.append(pylatex.NoEscape('\\mathbb{L} = \\{('))
    doc.append(", ".join(
        map(str, map(int, lsg))
        ))
    doc.append(pylatex.NoEscape(')\\}'))
    doc.append(pylatex.Command(')'))


if __name__ == "__main__":
    np.random.seed(10)
    doc_ue = pylatex.Document('lgs_ue', documentclass='article', document_options='a4paper')
    doc_lsg = pylatex.Document('lgs_lsg', documentclass='article', document_options='a4paper')

    doc_ue.preamble.append(pylatex.Command('title', 'Mathe 1 Übungen'))
    doc_lsg.preamble.append(pylatex.Command('title', 'Mathe 1 Lösungen'))
    for d in [doc_ue, doc_lsg]:
        d.preamble.append(pylatex.Command('author', 'Christian Henkel'))
        d.preamble.append(pylatex.Command('usepackage', 'amsfonts'))
        d.preamble.append(pylatex.Command('date', pylatex.NoEscape(r'\today')))
        d.append(pylatex.Command('maketitle'))
    lsgen = []
    sec = 'LGS'
    with doc_ue.create(pylatex.Section(sec)):
        with doc_ue.create(pylatex.Subsection('Eine Lösung')):
            doc_ue.append("Lösen Sie mit Gauß-Elimination die folgenden Gleichungsysteme:\n")
            doc_ue.append("(Tipp: Alle haben ")
            doc_ue.append(pylatex.utils.bold('genau eine '))
            doc_ue.append("Lösung.)")
            with doc_ue.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
                for i in range(2):
                    append_an_lgs(doc_ue, lsgen, 2, 2)
                for i in range(4):
                    append_an_lgs(doc_ue, lsgen, 3, 3)
                for i in range(3):
                    append_an_lgs(doc_ue, lsgen, 4, 4)
    with doc_lsg.create(pylatex.Section(sec)):
        with doc_lsg.create(pylatex.Subsection('Eine Lösung')):
            with doc_lsg.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
                for l in lsgen:
                    append_an_lsg(doc_lsg, l)
    for d in [doc_ue, doc_lsg]:
        d.generate_pdf(clean_tex=False)

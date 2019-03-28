# coding=utf-8
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


def goal_check(A, x, no_solution, inf_solutions, homogen):
    if homogen:
        b = np.zeros([A.shape[0], x.T.shape[1]])
        inf_solutions = random.randint(0, 1)
    else:
        b = np.dot(A, x.T)
        if (np.count_nonzero(b == 0) == A.shape[0]):
            return np.array([]), x
    if no_solution or inf_solutions:
        if not homogen:
            b = b + np.round(np.random.rand(1, b.shape[1]) * 2 - 1)
        n = A.shape[0]
        if no_solution:
            if not (np.linalg.matrix_rank(A) != np.linalg.matrix_rank(
                np.append(A, b, axis=1)
            )):
                x = ['no']
                return np.array([]), x
        if inf_solutions:
            line1 = random.randint(0, A.shape[1]-1)
            line2 = random.randint(0, A.shape[1]-1)
            while line1 == line2:
                line2 = random.randint(0, A.shape[1]-1)
            mult = random.choice([-3, -2, -1, 2, 3])
            A[line1, :] = mult * A[line2, :]
            b[line1] = mult * b[line2]
            if not (np.linalg.matrix_rank(A) == np.linalg.matrix_rank(
                np.append(A, b, axis=1)
            ) & np.linalg.matrix_rank(A) < n):
                x = ['inf']
                return np.array([]), x
    if(
        (np.max(b) <= 2)
        & (np.min(b) >= -2)
        & (np.count_nonzero(A == 0) <= 1)
    ):
        return b, x
    else:
        return np.array([]), x


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


def get_a_lgs(eqns, vars, no_or_inf_solutions, homogen):
    b = np.array([])
    while not len(b):
        A = rand_nice_numbers(eqns, vars)
        x = rand_nice_numbers(1, vars)
        if homogen:
            x = np.zeros([1, vars])
        if no_or_inf_solutions:
            no_solution, inf_solutions = random.choice(
                [(False, False), (True, False), (False, True)]
            )
            b, x = goal_check(A, x, no_solution, inf_solutions, homogen)
        else:
            b, x = goal_check(A, x, False, False, homogen)
    return make_tex(A, x, b), x[0]


def append_a_lgs(doc, lsgen, eqns, vars, no_or_inf_solutions=False, homogen=False):
    doc.append(pylatex.Command('item'))
    doc.append(pylatex.Command('('))
    doc.append(pylatex.Command('displaystyle'))
    with doc.create(Array(options="t", arguments="rrrrrr")):
        ue, lsg = get_a_lgs(eqns, vars, no_or_inf_solutions, homogen)
        doc.append(ue)
        lsgen.append(lsg)
    doc.append(pylatex.Command(')'))


def append_a_lsg(doc, lsg):
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
    sec = 'Lineare Gleichungsysteme mit einer Lösung'
    with doc_ue.create(pylatex.Section(sec)):
        lsgen_one = []
        with doc_ue.create(pylatex.Subsection('Vollständig Bestimmt')):
            doc_ue.append("Lösen Sie mit Gauß-Elimination die folgenden Gleichungsysteme:\n")
            doc_ue.append("(Tipp: Alle haben ")
            doc_ue.append(pylatex.utils.bold('genau eine '))
            doc_ue.append("Lösung.)")
            with doc_ue.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
                for i in range(2):
                    append_a_lgs(doc_ue, lsgen_one, 2, 2)
                for i in range(4):
                    append_a_lgs(doc_ue, lsgen_one, 3, 3)
                for i in range(3):
                    append_a_lgs(doc_ue, lsgen_one, 4, 4)
        lsgen_ueb = []
        with doc_ue.create(pylatex.Subsection('Überbestimmt')):
            doc_ue.append("Lösen Sie die folgenden überbestimmten Gleichungsysteme:\n")
            doc_ue.append("(Tipp: Alle haben ")
            doc_ue.append(pylatex.utils.bold('genau eine '))
            doc_ue.append("Lösung.)")
            with doc_ue.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
                for i in range(2):
                    append_a_lgs(doc_ue, lsgen_ueb, 3, 2)
                for i in range(2):
                    append_a_lgs(doc_ue, lsgen_ueb, 4, 3)
        lsgen_unt = []
        # with doc_ue.create(pylatex.Subsection('Unterbestimmt')):
        #     doc_ue.append("Lösen Sie die folgenden unterbestimmten Gleichungsysteme:\n")
        #     doc_ue.append("(Tipp: Alle haben ")
        #     doc_ue.append(pylatex.utils.bold('genau eine '))
        #     doc_ue.append("Lösung.)")
        #     with doc_ue.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
        #         for i in range(2):
        #             append_a_lgs(doc_ue, lsgen_unt, 2, 3)
        #         for i in range(2):
        #             append_a_lgs(doc_ue, lsgen_unt, 3, 4)
    # LÖSUNG
    with doc_lsg.create(pylatex.Section(sec)):
        with doc_lsg.create(pylatex.Subsection('Vollständig Bestimmt')):
            with doc_lsg.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
                for l in lsgen_one:
                    append_a_lsg(doc_lsg, l)
        with doc_lsg.create(pylatex.Subsection('Überbestimmt')):
            with doc_lsg.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
                for l in lsgen_ueb:
                    append_a_lsg(doc_lsg, l)
        # with doc_lsg.create(pylatex.Subsection('Unterbestimmt')):
        #     with doc_lsg.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
        #         for l in lsgen_unt:
        #             append_a_lsg(doc_lsg, l)
    # ---------------------------------------------------------------------------
    sec = 'Lineare Gleichungsysteme mit anderenen Lösungsmengen'
    with doc_ue.create(pylatex.Section(sec)):
        lsgen_diff = []
        with doc_ue.create(pylatex.Subsection('Übungen')):
            doc_ue.append("Bestimmen Sie die Lösungsmenge folgender Gleichungsysteme:\n")
            with doc_ue.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
                for i in range(4):
                    append_a_lgs(doc_ue, lsgen_diff, 2, 2, True, False)
                for i in range(4):
                    append_a_lgs(doc_ue, lsgen_diff, 3, 3, True, False)
    # LÖSUNG
    with doc_lsg.create(pylatex.Section(sec)):
        with doc_lsg.create(pylatex.Subsection('Übungen')):
            with doc_lsg.create(Enumerate(options=pylatex.NoEscape("label={\\alph*)}"))):
                for l in lsgen_diff:
                    append_a_lsg(doc_lsg, l)

    for d in [doc_ue, doc_lsg]:
        d.generate_pdf(clean_tex=True)

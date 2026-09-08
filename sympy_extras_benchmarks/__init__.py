"""Benchmark datasets and drivers for `sympy-extras
<https://github.com/Upabjojr/sympy-extras>`_.

``sympy_extras_benchmarks.datasets`` holds the parsers of the external
collections (the Kamke and Murphy ODE collections from Maxima's test
suite, the SMT-LIB ``QF_NRA`` Meti-Tarski problems) and the tables
translated into SymPy expressions (classical PDEs with their symmetry
algebras, the Katsura and cyclic polynomial systems).
``sympy_extras_benchmarks.drivers`` runs the algorithms of sympy-extras
on them and checks the results against the recorded answers.
"""
from __future__ import annotations

__version__ = '0.1.0'

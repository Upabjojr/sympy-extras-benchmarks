"""Parsers of the languages the benchmark collections are written in.

A parser reads the language of another system and returns SymPy objects.
It takes text, never a path; it reads no file and touches no network; it
does not know which collection the text comes from; and it does not decide
what a test suite asserts — which entries are claims, which proofs were
accepted, which recorded value is the answer. All of that is the business
of :mod:`sympy_extras_benchmarks.datasets`, which finds the files, reads
their structure and calls a parser on the source text they hold.

==========  ======================================================
Module      Language
==========  ======================================================
maxima      Maxima expressions, relations and source text
reduce      REDUCE expressions, rewritten into Maxima's syntax
fricas      FriCAS input, rewritten into Maxima's syntax
holpy       holpy expressions and integrals, read through Maxima's
maple       Maple polynomials
smtlib      SMT-LIB 2: ``QF_NRA``, and the arithmetic logics with
            integers and quantifiers
qepcad      the formula language of QEPCAD B and Tarski, and QEPCAD's
            input dialogue
prover      the arithmetic grammar Lean and Rocq statements share
lean        Lean 4 ``example`` statements
rocq        Rocq (Coq) ``Lemma``/``Goal`` statements
tptp        TPTP problems in TFF
==========  ======================================================

A parser refuses what it cannot translate faithfully — returning ``None``,
a reason, or raising its syntax error — rather than approximating it.
"""

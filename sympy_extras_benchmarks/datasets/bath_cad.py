"""The CAD example bank of the University of Bath.

D. Wilson, *Real Geometry and Connectedness via Triangular Description: CAD
Example Bank*, version 4 (2013), University of Bath Research Data Archive,
doi:10.15125/BATH-00069, licence CC BY-SA 4.0; described in R. Bradford, J.
H. Davenport, D. Wilson, M. England, *A repository for CAD examples*, ACM
Communications in Computer Algebra 46(3), 2012.

The archive has three files: the examples as QEPCAD inputs (78, of which a
few are repeated in two sections), the polynomials and variable lists of
the examples as a Maple file, and a PDF which states each example with its
suggested variable order and the best number of cells of a full CAD that
Maple achieved. They are downloaded on first use into the cache (or read
from ``$SYMPY_EXTRAS_BENCHMARKS_BATH_CAD``). The QEPCAD inputs are read with
:mod:`~sympy_extras_benchmarks.datasets.qepcad_syntax`; the bank records
no quantifier-free answers, so a result has to be checked against another
system. The cell counts are Maple's best, not a minimum a correct CAD must
reach, and are read only to be reported beside ours.
"""
from __future__ import annotations

import os
import pathlib
import re
import shutil
import subprocess
import urllib.request
from typing import Optional

from sympy import Symbol
from sympy.core.expr import Expr
from sympy.parsing.sympy_parser import parse_expr

from sympy_extras._typing import as_expr
from sympy_extras_benchmarks.cache import cache_directory
from sympy_extras_benchmarks.datasets.qepcad_syntax import Example, blocks

__all__ = ['FILES', 'ENVIRONMENT_VARIABLE', 'fetch', 'examples', 'PolynomialExample',
           'polynomial_examples', 'cell_counts']

#: the files of the archive and where they are published
FILES: dict[str, str] = {
    'QEPCADexamplebank_v4.txt': 'https://researchdata.bath.ac.uk/69/3/QEPCADexamplebank_v4.txt',
    'examplebank_v4.txt': 'https://researchdata.bath.ac.uk/69/2/examplebank_v4.txt',
    'examplebank_v4.pdf': 'https://researchdata.bath.ac.uk/69/1/examplebank_v4.pdf',
}

ENVIRONMENT_VARIABLE = 'SYMPY_EXTRAS_BENCHMARKS_BATH_CAD'


def fetch() -> Optional[pathlib.Path]:
    """The directory holding the three files, downloaded on first use."""
    override = os.environ.get(ENVIRONMENT_VARIABLE)
    if override and pathlib.Path(override).is_dir():
        return pathlib.Path(override)
    directory = cache_directory() / 'bath-cad-examples'
    try:
        directory.mkdir(parents=True, exist_ok=True)
        for name, url in FILES.items():
            target = directory / name
            if not target.exists():
                with urllib.request.urlopen(url, timeout=120) as response, open(target, 'wb') as sink:
                    shutil.copyfileobj(response, sink)
    except OSError:
        return None
    return directory


def examples() -> list[Example]:
    """The QEPCAD inputs of the bank, named by their position and title.
    An input repeated verbatim in a later section is marked as a duplicate
    of its first occurrence."""
    directory = fetch()
    if directory is None:
        return []
    text = (directory / 'QEPCADexamplebank_v4.txt').read_text(errors='replace')
    found: list[Example] = []
    first: dict[str, str] = {}
    for index, (match, _) in enumerate(blocks(text), 1):
        source = match.group(0)
        name = '%02d %s' % (index, match.group('name').strip())
        body = re.sub(r'\s+', ' ', source.split('\n', 1)[1])
        found.append(Example('bath', name, 'qepcad', source, duplicate_of=first.get(body)))
        first.setdefault(body, 'bath/' + name)
    return found


class PolynomialExample:
    """The polynomials and the variable list of an example of the Maple file
    (the list is in Maple's order: the first variable is the greatest)."""

    def __init__(self, section: str, number: int, title: str, polynomials: list[Expr],
                 variables: list[Symbol]) -> None:
        self.section = section
        self.number = number
        self.title = title
        self.polynomials = polynomials
        self.variables = variables

    def __repr__(self) -> str:
        return "PolynomialExample(%s #%d %r)" % (self.section, self.number, self.title)


def _maple(text: str, symbols: dict[str, Symbol]) -> Expr:
    for name in re.findall(r'[A-Za-z_][A-Za-z0-9_]*', text):
        symbols.setdefault(name, Symbol(name))
    local: dict[str, object] = dict(symbols)
    return as_expr(parse_expr(text.replace('^', '**'), local_dict=local))


def polynomial_examples() -> list[PolynomialExample]:
    """The examples of the Maple file which are lists of polynomials."""
    directory = fetch()
    if directory is None:
        return []
    text = (directory / 'examplebank_v4.txt').read_text(errors='replace')
    found: list[PolynomialExample] = []
    for section, body in re.findall(r'^(\w+)Examples:=proc\(n\)(.*?)^end:', text, re.M | re.S):
        for number, title, polys, variables in re.findall(
                r'#(\d+):[ \t]*([^\n]*)\n\s*\[\[([^\[\]]*)\],\s*\[([^\[\]]*)\]\]', body):
            symbols: dict[str, Symbol] = {}
            names = [v.strip() for v in variables.split(',') if v.strip()]
            for v in names:
                symbols.setdefault(v, Symbol(v))
            polynomials = [_maple(p, symbols) for p in polys.split(',') if p.strip()]
            found.append(PolynomialExample(section, int(number), title.strip(), polynomials,
                                           [symbols[v] for v in names]))
    return found


def cell_counts() -> dict[str, tuple[int, list[str]]]:
    """Maple's best number of cells for each example of the PDF, with the
    variable order it was achieved with (Maple's order), keyed by the title
    in lower case; empty when ``pdftotext`` is not installed."""
    directory = fetch()
    if directory is None or shutil.which('pdftotext') is None:
        return {}
    try:
        text = subprocess.run(['pdftotext', '-layout', str(directory / 'examplebank_v4.pdf'), '-'],
                              check=True, capture_output=True, text=True, timeout=120).stdout
    except (OSError, subprocess.SubprocessError):
        return {}
    return _read_counts(text)


def _read_counts(text: str) -> dict[str, tuple[int, list[str]]]:
    """The cell counts of the text of the PDF, with the variable order (in
    Maple's order, greatest first) they were achieved with; the order is
    empty when the PDF does not say. Each example is a section headed
    ``n.m Title``, and a count is read only inside its own section, since
    several examples leave it blank. The order is the bracketed list after
    "variable ordering", or the "Suggested variable order" of the section
    when the count was achieved with it.

    >>> from sympy_extras_benchmarks.datasets.bath_cad import _read_counts
    >>> text = '''2.1  Parabola
    ...    Suggested variable order: x > c > b > a.
    ...    Best achieved number of cells: 27 - with Maple and variable ordering
    ... [x,c,b,a] (that is, x > c > b > a).
    ... 2.2  Umbrella
    ...    Best achieved number of cells:
    ...    Source: [CMXY09]
    ... 2.3  Solotareff
    ...    Suggested variable order: v > u > b > r > a
    ...    Best achieved number of cells: 207 (Maple with suggested ordering).
    ...    Source: [Ach56]
    ... 2.4  Other
    ...    Best achieved number of cells: 12
    ... '''
    >>> for title, value in sorted(_read_counts(text).items()):
    ...     print(title, value)
    other (12, [])
    parabola (27, ['x', 'c', 'b', 'a'])
    solotareff (207, ['v', 'u', 'b', 'r', 'a'])
    """
    counts: dict[str, tuple[int, list[str]]] = {}
    headings = list(re.finditer(r'^\s*\d+\.\d+\s+(\S[^\n]*?)\s*$', text, re.M))
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        section = text[heading.end():end]
        count = re.search(r'number of cells:[ \t]*(\d+)', section)
        if count is None:
            continue
        order: list[str] = []
        stated = re.search(r'variable\s+ordering\s*\[([^\]]*)\]', section[count.start():])
        suggested = re.search(r'Suggested variable order:[ \t]*([^\n]*)', section)
        if stated is not None:
            order = [v.strip() for v in stated.group(1).split(',') if v.strip()]
        elif 'suggested' in section[count.start():count.start() + 200].lower() and suggested is not None:
            order = [v.strip(' .') for v in suggested.group(1).split('>') if v.strip(' .')]
        counts.setdefault(heading.group(1).strip().lower(), (int(count.group(1)), order))
    return counts

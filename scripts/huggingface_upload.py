"""Stage the collections too large for ``data/`` and upload them to the
Hugging Face Hub.

Three collections are not kept in the repository (see ``data/README.md``).
This script puts each into a dataset repository of its own, because each
has its own licence and a Hub dataset card declares exactly one:

``smtlib-2025-nra``
    The ``QF_NRA`` and ``NRA`` archives of the SMT-LIB 2025 release, as
    Zenodo publishes them (``.tar.zst``, checked against Zenodo's MD5
    sums). CC BY 4.0.
``tarski-brown-vale-enriquez-2019``
    The data of C. W. Brown and F. Vale-Enriquez (2019) from Tarski's
    repository: ``smtlib-r1`` and ``smtlib-r2`` packed as one ``.tar.zst``
    each (139000 files is more than a Hub repository should hold as
    loose files), with ``round1inputs``, ``round2inputs`` and ``README``
    as they are. ISC licence.
``z3test-nl-large``
    The two machine-generated files of ``z3test``'s ``regressions/nl``
    (13 MB and 9 MB). MIT licence.

Every file keeps its source language (SMT-LIB 2, and the formula lists of
Tarski); nothing is translated. The licence text of each upstream and a
dataset card with the attribution are written beside the data, and
``SHA256SUMS`` lists every file.

Usage::

    python scripts/huggingface_upload.py                      # stage all three
    python scripts/huggingface_upload.py --only z3test-nl-large
    hf auth login                                             # once
    python scripts/huggingface_upload.py --upload --namespace NAME [--public]

Staging reads the downloads of the cache, making them first through the
dataset modules when they are missing, and writes to
``.cache/huggingface-staging/`` (gitignored). ``--upload`` creates the
dataset repositories, **private unless** ``--public`` is given, and sends
each staged directory with ``upload_large_folder``, which resumes an
interrupted upload. ``huggingface_hub`` is needed only for ``--upload``.

The repositories are published under the ``Upabjojr`` namespace:
https://huggingface.co/datasets/Upabjojr/smtlib-2025-nra,
https://huggingface.co/datasets/Upabjojr/tarski-brown-vale-enriquez-2019 and
https://huggingface.co/datasets/Upabjojr/z3test-nl-large.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import shutil
import subprocess
import sys
from typing import Callable, Optional

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sympy_extras_benchmarks.cache import cache_directory, data_directory  # noqa: E402

#: the default directory the repositories are staged in
STAGING = 'huggingface-staging'


def _sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def _md5(path: pathlib.Path) -> str:
    digest = hashlib.md5()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def _copy(source: pathlib.Path, target: pathlib.Path) -> None:
    if target.exists() and target.stat().st_size == source.stat().st_size:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def _pack(parent: pathlib.Path, name: str, target: pathlib.Path, level: int) -> None:
    """``parent/name`` as a reproducible ``.tar.zst``: sorted names, no
    owners, a fixed time, so the same tree always gives the same bytes."""
    if target.exists():
        return
    partial = target.with_name(target.name + '.partial')
    with open(partial, 'wb') as sink:
        tar = subprocess.Popen(
            ['tar', '--sort=name', '--mtime=@0', '--owner=0', '--group=0', '--numeric-owner',
             '-C', str(parent), '-cf', '-', name], stdout=subprocess.PIPE)
        zstd = subprocess.run(['zstd', '-%d' % level, '-T0', '-q', '-c'],
                              stdin=tar.stdout, stdout=sink, check=False)
        if tar.stdout is not None:
            tar.stdout.close()
        if tar.wait() != 0 or zstd.returncode != 0:
            partial.unlink()
            raise RuntimeError('packing %s failed' % (parent / name))
    partial.rename(target)


def _checksums(directory: pathlib.Path) -> None:
    lines = ['%s  %s' % (_sha256(path), path.relative_to(directory).as_posix())
             for path in sorted(directory.rglob('*'))
             if path.is_file() and path.name != 'SHA256SUMS'
             and not path.relative_to(directory).as_posix().startswith('.cache/')]
    (directory / 'SHA256SUMS').write_text('\n'.join(lines) + '\n')


def _card(directory: pathlib.Path, licence: str, pretty_name: str, body: str) -> None:
    front = '\n'.join(['---', 'license: %s' % licence, 'pretty_name: "%s"' % pretty_name,
                       'tags:', '- smt-lib', '- nonlinear-real-arithmetic', '- sympy-extras-benchmarks',
                       '---', ''])
    (directory / 'README.md').write_text(front + body.lstrip())


def stage_smtlib(target: pathlib.Path, level: int) -> None:
    from sympy_extras_benchmarks.datasets import smtlib_release
    root = cache_directory() / 'smtlib-2025'
    for logic, (name, md5) in smtlib_release.ARCHIVES.items():
        archive = root / name
        if not archive.is_file() and smtlib_release.fetch(logic) is None:
            raise RuntimeError('the %s archive could not be downloaded' % logic)
        if _md5(archive) != md5:
            raise RuntimeError('%s does not match the MD5 sum Zenodo publishes' % archive)
        _copy(archive, target / name)
    _card(target, 'cc-by-4.0', 'SMT-LIB 2025: QF_NRA and NRA', """
# SMT-LIB release 2025: `QF_NRA` and `NRA`

The two nonlinear real arithmetic logics of the SMT-LIB 2025 release of the
non-incremental benchmarks, **unchanged**: the archives are the ones Zenodo
publishes, byte for byte (their MD5 sums are the published ones; `SHA256SUMS`
lists them too).

| File | Logic | Problems |
|---|---|---|
| `QF_NRA.tar.zst` | quantifier-free nonlinear real arithmetic, 16 families | 12154 (5257 sat, 5536 unsat, 1361 unknown) |
| `NRA.tar.zst` | quantified nonlinear real arithmetic | 3819 (3806 unsat, 5 sat, 8 unknown) |

Unpack with `tar --zstd -xf QF_NRA.tar.zst`. The problems are SMT-LIB 2 files,
each with its `:status`.

## Source and licence

    SMT-LIB release 2025 (non-incremental benchmarks)
    Mathias Preiner, Hans-Jorg Schurr, Clark Barrett, Pascal Fontaine,
    Aina Niemetz and Cesare Tinelli. Zenodo, 2025.
    doi:10.5281/zenodo.16740866

Distributed under the **Creative Commons Attribution 4.0 International**
licence, as on Zenodo. This copy exists so that
[sympy-extras-benchmarks](https://github.com/Upabjojr/sympy-extras-benchmarks)
can fetch the release from the Hub; please cite the release above.
""")


def stage_brown(target: pathlib.Path, level: int) -> None:
    from sympy_extras_benchmarks.datasets import tarski_tests
    root = tarski_tests.fetch(tarski_tests.BROWN_SUBTREE)
    if root is None or not (root / tarski_tests.BROWN_SUBTREE).is_dir():
        raise RuntimeError('the Brown--Vale-Enriquez data could not be downloaded')
    source = root / tarski_tests.BROWN_SUBTREE
    for name in ('README', 'round1inputs', 'round2inputs'):
        _copy(source / name, target / name)
    for name in ('smtlib-r1', 'smtlib-r2'):
        print('packing %s (this takes a while)' % name, flush=True)
        _pack(source, name, target / (name + '.tar.zst'), level)
    licence = data_directory() / 'tarski' / 'interpreter' / 'LICENSE'
    _copy(licence, target / 'LICENSE')
    _card(target, 'isc', 'Brown and Vale-Enriquez 2019: QF_NRA conjunctions', """
# Brown and Vale-Enriquez (2019): conjunctions of nonlinear real constraints

The data sets of C. W. Brown and F. Vale-Enriquez, *From Simplification to a
Partial Theory Solver for Non-Linear Real Polynomial Constraints* (2019), as
kept in the `tests/dataset-Brown-V-E-2019` directory of
[Tarski](https://github.com/chriswestbrown/tarski).

| File | Content |
|---|---|
| `smtlib-r1.tar.zst` | round 1: 19555 SMT-LIB 2 files, the disjuncts of the DNF of Meti-Tarski problems of SMT-LIB `QF_NRA` |
| `smtlib-r2.tar.zst` | round 2: 119395 SMT-LIB 2 files, from the simplified equivalents of the round 1 formulas |
| `round1inputs`, `round2inputs` | the same formulas, one per line, as `<name> : <formula>` in Tarski's syntax |
| `README` | the authors' description, unchanged |

The two directories are packed only because 139000 loose files are more than a
Hub repository should hold; the files inside are unchanged. Unpack with
`tar --zstd -xf smtlib-r1.tar.zst`. The problems carry no status; a disjunct of
an unsatisfiable Meti-Tarski problem is unsatisfiable, and its source is the
Meti-Tarski file its name starts with.

## Source and licence

Copied from Tarski's repository, whose licence (`LICENSE`, an ISC licence,
Copyright (c) 2015 Chris Brown) covers it. Please cite the paper above.
""")


def stage_z3(target: pathlib.Path, level: int) -> None:
    from sympy_extras_benchmarks.datasets import solver_regressions
    clone = cache_directory() / 'solver-regressions-z3'
    names = ('fastmul-unfolded-l-native-nl-wrapped.smt2', 'helperlemma-l-native-nl-wrapped.smt2')
    directory = clone / 'regressions' / 'nl'
    if not all((directory / n).is_file() for n in names):
        # the kept copy in data/ lacks exactly these files, so clone past it
        repository, subtrees = solver_regressions.SOURCES['z3']
        subprocess.run(['git', 'clone', '--depth', '1', '--filter=blob:none', '--sparse',
                        repository, str(clone)], check=False, capture_output=True, timeout=1800)
        subprocess.run(['git', '-C', str(clone), 'sparse-checkout', 'set', *subtrees],
                       check=False, capture_output=True, timeout=1800)
    for name in names:
        if not (directory / name).is_file():
            raise RuntimeError('%s could not be downloaded' % (directory / name))
        _copy(directory / name, target / 'regressions' / 'nl' / name)
    _copy(data_directory() / 'solver-regressions-z3' / 'LICENSE.txt', target / 'LICENSE.txt')
    _card(target, 'mit', 'z3test: large nonlinear regressions', """
# z3test: the two large nonlinear regressions

Two machine-generated SMT-LIB 2 files of the `regressions/nl` directory of
[z3test](https://github.com/Z3Prover/z3test), unchanged and at the same paths:

| File | Size |
|---|---|
| `regressions/nl/fastmul-unfolded-l-native-nl-wrapped.smt2` | 13 MB |
| `regressions/nl/helperlemma-l-native-nl-wrapped.smt2` | 9 MB |

The rest of the directory is small and is kept in
[sympy-extras-benchmarks](https://github.com/Upabjojr/sympy-extras-benchmarks)
itself; these two are hosted here only because of their size.

## Source and licence

Copyright (c) Microsoft Corporation, distributed under the **MIT** licence
(`LICENSE.txt`, as in z3test).
""")


#: the repositories: name, staging function
COLLECTIONS: dict[str, Callable[[pathlib.Path, int], None]] = {
    'smtlib-2025-nra': stage_smtlib,
    'tarski-brown-vale-enriquez-2019': stage_brown,
    'z3test-nl-large': stage_z3,
}


def upload(directory: pathlib.Path, repository: str, public: bool) -> None:
    from huggingface_hub import HfApi
    api = HfApi()
    api.create_repo(repository, repo_type='dataset', private=not public, exist_ok=True)
    api.upload_large_folder(repo_id=repository, folder_path=str(directory), repo_type='dataset')


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0],
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--only', choices=sorted(COLLECTIONS), action='append',
                        help='stage (and upload) only this collection; may be repeated')
    parser.add_argument('--staging', type=pathlib.Path,
                        help='where to stage (default: .cache/%s)' % STAGING)
    parser.add_argument('--level', type=int, default=19, help='zstd level of the packed trees')
    parser.add_argument('--upload', action='store_true', help='upload after staging')
    parser.add_argument('--namespace', help='Hub user or organisation (default: the logged-in user)')
    parser.add_argument('--public', action='store_true', help='create public repositories (default: private)')
    args = parser.parse_args(argv)
    staging: pathlib.Path = args.staging or cache_directory() / STAGING
    names: list[str] = args.only or list(COLLECTIONS)
    for name in names:
        target = staging / name
        target.mkdir(parents=True, exist_ok=True)
        print('staging %s in %s' % (name, target), flush=True)
        try:
            COLLECTIONS[name](target, args.level)
        except (RuntimeError, OSError) as error:
            print('%s: %s' % (name, error), file=sys.stderr)
            return 1
        _checksums(target)
        size = sum(p.stat().st_size for p in target.rglob('*') if p.is_file())
        print('  %d files, %.1f MB' % (sum(1 for p in target.rglob('*') if p.is_file()), size / 1048576))
    if not args.upload:
        print('staged; run again with --upload to send them to the Hub')
        return 0
    namespace: Optional[str] = args.namespace
    if namespace is None:
        from huggingface_hub import HfApi
        namespace = str(HfApi().whoami()['name'])
    for name in names:
        repository = '%s/%s' % (namespace, name)
        print('uploading %s to https://huggingface.co/datasets/%s' % (staging / name, repository), flush=True)
        upload(staging / name, repository, args.public)
    return 0


if __name__ == '__main__':
    sys.exit(main())

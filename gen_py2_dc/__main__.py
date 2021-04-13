import argparse
from pathlib import Path
from typing import Iterable, List

from gen_py2_dc import parse_input, gen_py_body, gen_pyi_body


def _parse_arg() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Generate dataclass style class definition for Python 2.')
    parser.add_argument(
        'pyi',
        metavar='PYI',
        type=Path,
        nargs='+',
        help='File or folder to add comment ' '(Folders are recursively browsed and support wildcard * amd **)',
    )

    return parser.parse_args()


def main(paths: Iterable[Path]) -> None:
    for path in paths:
        py_body: List[str] = []
        pyi_body: List[str] = []
        for class_def in parse_input(path.read_text()):
            py_body.append(gen_py_body(class_def))
            pyi_body.append(gen_pyi_body(class_def))

        print('\n\n'.join(py_body))
        print('------------------------')
        print('\n\n'.join(pyi_body))


if __name__ == '__main__':
    arg = _parse_arg()
    main(arg.pyi)

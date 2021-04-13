from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Iterable, Sequence, Tuple

from jinja2 import Environment, PackageLoader, select_autoescape

Pair = Tuple[str, str]


@dataclass
class Class:
    name: str
    fields: Sequence[Pair]


_jinja_env = Environment(
    loader=PackageLoader('gen_py2_dc'),
    autoescape=select_autoescape(('jinja2',)),
)


def gen_py_body(conf: Class) -> str:
    return _jinja_env.get_template('py.jinja2').render(
        class_name=conf.name,
        fields=conf.fields,
    )


def gen_pyi_body(conf: Class) -> str:
    return _jinja_env.get_template('pyi.jinja2').render(
        class_name=conf.name,
        fields=conf.fields,
    )


def parse_input(class_def: str) -> Iterable[Class]:
    result: ast.Module = ast.parse(class_def)

    for class_def in result.body:
        if not isinstance(class_def, ast.ClassDef):
            continue

        yield Class(
            name=class_def.name,
            fields=tuple(
                (ast.unparse(assign.target), ast.unparse(assign.annotation))
                for assign in class_def.body
                if isinstance(assign, ast.AnnAssign)
            ),
        )

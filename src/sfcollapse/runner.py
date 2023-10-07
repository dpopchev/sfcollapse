"""run scalar field collapse notebook"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

if TYPE_CHECKING:
    from argparse import ArgumentParser


def copy_into(source: Path, destination: Path) -> None:
    """copy file using pathlib.Path"""
    destination.joinpath(source.name).write_text(source.read_text())


def mark_notebook_executed(nb_path: Path) -> None:
    """due to the notebook mechanism preserve the cell output into .executed nb"""

    return nb_path.parent / f"{nb_path.stem}.executed"


def execute_notebook(nb_path: Path) -> None:
    """execution driver for a notebook found in path"""

    preprocessor = ExecutePreprocessor(
        timeout=600,
        kernel_name='python3',
        enabled=True,
    )
    resources = {'metadata': {'path': nb_path.parent}}

    with open(nb_path, encoding='utf-8') as nb_handler:
        nb_inmemory = nbformat.read(nb_handler, as_version=4)

        preprocessor(nb_inmemory, resources)

        with open(mark_notebook_executed(nb_path), 'w', encoding='utf-8') as executed_handler:
            nbformat.write(nb_inmemory, executed_handler)


def sandbox_run(
    notebook: Path,
    config: Path,
    destination: Path = Path('build'),
    ) -> None:
    """run notebook in sandbox"""
    destination.mkdir(parents=True, exist_ok=True)
    copy_into(notebook, destination)
    copy_into(config, destination)
    execute_notebook(destination.joinpath(notebook.name))


def hydrate_parser(parser: ArgumentParser):
    parser.add_argument(
        '-nb', '--notebook',
        help='notebook implementation of the collapse simulation',
        default='dpopchev/scalar_field_collapse.ipynb',
        type=Path,
    )
    parser.add_argument(
        '-c', '--config',
        help='notebook configuration',
        default='dpopchev/scalar_field_collapse.ini',
        type=Path,
    )
    parser.add_argument(
        '-s', '--sandbox',
        default='build',
        help='destination to execute the notebook and store results',
        type=Path,
    )

    parser.set_defaults(
        driver=lambda _: sandbox_run(
            _.notebook,
            _.config,
            _.sandbox,
        ),
    )

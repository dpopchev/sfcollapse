"""run scalar field collapse notebook"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import nbformat
from nbconvert.preprocessors.execute import ExecutePreprocessor

if TYPE_CHECKING:
    from configparser import ConfigParser


def mark_notebook_executed(nb_path: Path) -> Path:
    """due to the notebook mechanism preserve the cell output into .executed nb"""
    return nb_path.parent / f"{nb_path.stem}_executed{nb_path.suffix}"


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

def sandbox_notebook(nb: Path, mark: str = 'sandbox') -> Path:
    sandboxed_nb = nb.parent.joinpath(f"{mark}_{nb.name}")
    sandboxed_nb.write_text(nb.read_text())
    return sandboxed_nb

def make_notebook_config(nb: Path, config:ConfigParser) -> None:
    with open(nb.parent.joinpath(f"{nb.stem}.ini"), 'w') as config_handler:
        config.write(config_handler)

def sandbox_run(
    notebook: Path,
    config: ConfigParser
    ) -> None:
    """run notebook in sandbox"""
    make_notebook_config(notebook, config)
    execute_notebook(sandbox_notebook(notebook))

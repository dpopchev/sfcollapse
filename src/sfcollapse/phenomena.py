from collections import namedtuple
from pathlib import Path
import re
from typing import Any
from sfcollapse.runner import make_config, sandbox_run, NOTEBOOK_NAME
from sfcollapse.data_aggregation import make_whitespace_reader, DataAggregator
from timeit import default_timer as timer
import logging

logger = logging.getLogger(__name__)

NotableRun = namedtuple('NotableRun', 'name amplitude')

NOTABLE_RUNS = [
    NotableRun('default', '0.4'),
    NotableRun('paper', '0.336426615643'),
    NotableRun('miguel', '0.3033260605'),
    NotableRun('dpguess1', '0.29'),
    NotableRun('dpguess2', '0.28'),
]

EXPLORE_RUNS = [
    NotableRun('left', '0.30340'),
    NotableRun('right','0.30359'),
]

DEFAULT_RUNS = EXPLORE_RUNS

PATTERN = re.compile(r'out640-(?P<seq>\d+).txt$')

reader = make_whitespace_reader(['xx0', 'rr', 'sf', 'sfm', 'alpha', 'cf', 'log10H'])

def make_data_home(run_name: str):
    return Path(f'{run_name}/output/')

def do_run(run, notebook = NOTEBOOK_NAME):
    logger.info(f'Running {run.name} with amplitude = {run.amplitude}')
    start = timer()
    sandbox_run(Path(notebook), make_config(name=run.name, amplitude=run.amplitude))
    logger.info(f'END {run.name}, time ellapsed = {timer() - start:.3f}s')

def run(runs: Any = DEFAULT_RUNS):
    for notable in runs:
        do_run(notable)

def make_run_aggregators(runs: Any = DEFAULT_RUNS):
    return {r.name: DataAggregator(make_data_home(r.name), PATTERN, reader=reader) for r in runs}

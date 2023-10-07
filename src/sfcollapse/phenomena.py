from collections import namedtuple
from pathlib import Path
import re
from typing import Any
from sfcollapse.runner import make_config, sandbox_run, NOTEBOOK_NAME
from sfcollapse.data_aggregation import make_whitespace_reader, DataAggregator
from timeit import default_timer as timer

NotableRun = namedtuple('NotableRun', 'name amplitude')

NOTABLE_RUNS = [
    NotableRun('default', '0.4'),
    NotableRun('paper', '0.336426615643'),
    NotableRun('miguel', '0.3033260605'),
    NotableRun('dpguess1', '0.29'),
    NotableRun('dpguess2', '0.28'),
]

PATTERN = re.compile(r'out640-(?P<seq>\d+).txt$')

reader = make_whitespace_reader(['xx0', 'rr', 'sf', 'sfm', 'alpha', 'cf', 'log10H'])

def make_data_home(run_name: str):
    return Path(f'{run_name}/output/')

def run(runs: Any = NOTABLE_RUNS):
    for notable in runs:
        print(f'Running {notable.name} with amplitude = {notable.amplitude}')
        start = timer()
        sandbox_run(Path(NOTEBOOK_NAME), make_config(name=notable.name, amplitude=notable.amplitude))
        print(f'END {notable.name}, time ellapsed = {timer() - start}')

def make_run_aggregators(runs: Any = NOTABLE_RUNS):
    return {r.name: DataAggregator(make_data_home(r.name), PATTERN, reader=reader) for r in runs}

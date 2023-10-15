import logging
import re
from collections import namedtuple
from pathlib import Path
from timeit import default_timer as timer
from typing import Any, Dict, Iterable

from sfcollapse.data_aggregation import DataAggregator, make_whitespace_reader
from sfcollapse.runner import NOTEBOOK_NAME, make_config, sandbox_run

logger = logging.getLogger(__name__)

NotableAmplitudeRun = namedtuple('NotableRun', 'name amplitude')

NOTABLE_AMPLITUDE_RUNS = (
    NotableAmplitudeRun('default', '0.4'),
    NotableAmplitudeRun('paper', '0.336426615643'),
    NotableAmplitudeRun('miguel', '0.3033260605'),
    NotableAmplitudeRun('dpguess1', '0.29'),
    NotableAmplitudeRun('dpguess2', '0.28'),
    NotableAmplitudeRun('exploretion-left', '0.30340'),
    NotableAmplitudeRun('exploration-right', '0.30359'),
)

EXPLORE_RUNS = (
    {'name': 'nx0-320', 'amplitude': '0.30340', 'nx0': '320'},
    {'name': 'nx0-640', 'amplitude': '0.30340', 'nx0': '640'},
    {'name': 'nx0-960', 'amplitude': '0.30340', 'nx0': '960'},
)

DEFAULT_RUNS = EXPLORE_RUNS

PATTERN = re.compile(r'out(?:\d+)-(?P<seq>\d+).txt$')

reader = make_whitespace_reader(
    ['xx0', 'rr', 'sf', 'sfm', 'alpha', 'cf', 'log10H'],
)


def make_data_home(run_name: str):
    return Path(f'{run_name}/output/')


def do_run(run, notebook=NOTEBOOK_NAME):
    logger.info(f'Running {run["name"]} with amplitude = {run["amplitude"]}')
    start = timer()
    sandbox_run(Path(notebook), make_config(**run))
    logger.info(f'END {run["name"]}, time ellapsed = {timer() - start:.3f}s')


def run(runs: Iterable[Dict] = DEFAULT_RUNS):
    for notable in runs:
        do_run(notable)


def make_run_aggregators(runs: Iterable[Dict] = DEFAULT_RUNS):
    return {
        r['name']: DataAggregator(
            make_data_home(
                r['name'],
            ),
            PATTERN,
            reader=reader,
        ) for r in runs
    }

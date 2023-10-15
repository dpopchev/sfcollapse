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
    {'name': 'nx0-640-nxrest4', 'amplitude': '0.30340', 'nx0': '640', 'nx1': '4', 'nx2': '4'},
    {'name': 'nx0-640-cfl_factor0.1', 'amplitude': '0.30340', 'cfl_factor': '0.1'},
    {'name': 'nx0-640', 'amplitude': '0.30340', 'nx0': '640'},
)

DEFAULT_RUNS = EXPLORE_RUNS

PATTERN = re.compile(r'out(?:\d+)-(?P<seq>\d+).txt$')

reader = make_whitespace_reader(
    ['xx0', 'rr', 'sf', 'sfm', 'alpha', 'cf', 'log10H'],
)

RUN_ELLAPSED_THRESHOLD = 65

def make_data_home(run_name: str):
    return Path(f'{run_name}/output/')


def do_run(run, notebook=NOTEBOOK_NAME):
    logger.info( f'Running %s with amplitude = %s',run["name"],run["amplitude"])
    start = timer()
    sandbox_run(Path(notebook), make_config(**run))
    ellapsed = timer() - start
    log_ellapsed = logger.info if ellapsed > RUN_ELLAPSED_THRESHOLD else logger.warn
    log_ellapsed(f'END %s, time ellapsed = %.2f', run["name"], ellapsed)


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

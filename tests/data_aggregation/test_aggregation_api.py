import re
from typing import Iterable

import pytest

from sfcollapse.data_aggregation import DataAggregator

PATH_CONTENT = ['out640-01.txt', 'out640-02.txt', 'out640-03.txt', 'out640.txt']
FILE_PATTERN = re.compile(r'out640-(\d+).txt')

@pytest.fixture
def make_path_stub(mocker):
    stub = mocker.Mock()

    def factory(iterdir: Iterable[str]):
        stub.iterdir.return_value = iterdir
        return stub

    return factory

@pytest.fixture
def aggregator(make_path_stub):
    return DataAggregator(make_path_stub(PATH_CONTENT), FILE_PATTERN)

def test_aggregator_finds_data_sources_using_pattern(aggregator):
    assert aggregator.sources == [
        'out640-01.txt',
        'out640-02.txt',
        'out640-03.txt',
    ]

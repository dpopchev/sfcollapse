import re
from typing import Iterable

import pytest

from sfcollapse.data_aggregation import DataAggregator


@pytest.fixture
def make_aggregator():
    return DataAggregator


@pytest.fixture
def make_path_stub(mocker):
    stub = mocker.Mock()

    def factory(iterdir: Iterable[str]):
        stub.iterdir.return_value = iterdir
        return stub
    return factory


def test_aggregator_finds_data_sources_using_pattern(
        make_aggregator, make_path_stub,
):
    pattern = re.compile(r'out640-(\d+).txt')
    content = ['out640-01.txt', 'out640-02.txt', 'out640-03.txt', 'out640.txt']
    aggregator = make_aggregator(make_path_stub(content), pattern)
    assert aggregator.sources == [
        'out640-01.txt',
        'out640-02.txt',
        'out640-03.txt',
    ]

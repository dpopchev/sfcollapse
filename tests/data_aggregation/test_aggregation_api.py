from __future__ import annotations

from pathlib import Path
import re
from typing import Iterable

import pytest

from sfcollapse.data_aggregation import DataAggregator, DataReader

from random import shuffle

class StubReader(DataReader):
    def __call__(self):
        ...

class TestAggregatorApi:
    PATH_PREFIX = 'somedir'
    PATH_CONTENT = ['out640-01.txt', 'out640-02.txt', 'out640-03.txt', 'out640.txt']
    FILE_PATTERN = re.compile(r'out640-(?P<seq>\d+).txt')

    @pytest.fixture(autouse=True)
    def randomize_path_content_order(self):
        shuffle(self.PATH_CONTENT)

    @pytest.fixture
    def make_path_stub(self, mocker):
        stub = mocker.Mock()

        def factory(path_prefix: str, iterdir: Iterable[str]):
            stub.iterdir.return_value = [Path(f"{path_prefix}/{d}") for d in iterdir]
            return stub

        return factory

    @pytest.fixture
    def aggregator(self, make_path_stub):
        return DataAggregator(
            make_path_stub(self.PATH_PREFIX, self.PATH_CONTENT),
            self.FILE_PATTERN,
            StubReader()
        )

    def test_data_sources_are_filtered_in_path(self, aggregator):
        assert aggregator.sources == [
            'out640-01.txt',
            'out640-02.txt',
            'out640-03.txt',
        ]

    def test_sequence_extracted_from_source_names(self, aggregator):
        assert aggregator.sequence == [1, 2, 3]

import re
from typing import Iterable

import pytest

from sfcollapse.data_aggregation import DataAggregator

class TestAggregatorApi:
    PATH_CONTENT = ['out640-01.txt', 'out640-02.txt', 'out640-03.txt', 'out640.txt']
    FILE_PATTERN = re.compile(r'out640-(\d+).txt')

    @pytest.fixture
    def make_path_stub(self, mocker):
        stub = mocker.Mock()

        def factory(iterdir: Iterable[str]):
            stub.iterdir.return_value = iterdir
            return stub

        return factory

    @pytest.fixture
    def aggregator(self, make_path_stub):
        return DataAggregator(make_path_stub(self.PATH_CONTENT), self.FILE_PATTERN)

    def test_data_sources_are_filtered_in_path(self, aggregator):
        assert aggregator.sources == [
            'out640-01.txt',
            'out640-02.txt',
            'out640-03.txt',
        ]

    def test_order_is_extracted_from_source_names(self, aggregator):
        pass

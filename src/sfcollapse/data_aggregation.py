from __future__ import annotations
from functools import partial

import pandas as pd

from dataclasses import dataclass
from typing import (
    TYPE_CHECKING, Dict, Iterable, Match, Pattern,
    Protocol, Sequence, Tuple, Union,
)

if TYPE_CHECKING:
    from pathlib import Path


class Stringable(Protocol):
    def __str__(self) -> str:
        ...

class DataReader(Protocol):
    def __call__(self, _: Path) -> pd.DataFrame:
        ...

@dataclass
class DataAggregator:
    _path: Path
    _pattern: Pattern
    reader: DataReader
    sequence_group: str = 'seq'

    def _make_match(self, text: Stringable) -> Union[Match, None]:
        return self._pattern.search(str(text))

    def _mask_sources(self) -> Iterable[Tuple[Path, Union[Match, None]]]:
        return [(p, self._make_match(p)) for p in self._path.iterdir()]

    def _get_sources(self) -> Dict[float, Path]:
        return dict(
            (float(m.group(self.sequence_group)), p)
            for p, m in self._mask_sources() if m
        )

    @property
    def sources(self) -> Sequence[str]:
        return sorted(p.name for p in self._get_sources().values())

    @property
    def sequence(self) -> Sequence[float]:
        return sorted(s for s in self._get_sources().keys())

    def get_data(self, sequence: float) -> pd.DataFrame:
        return self.reader(self._get_sources()[sequence])

    def get_data_chage(self, interval: Sequence[float], iloc: int = 0) -> pd.DataFrame:
        rows = []
        for seq in interval:
            rows.append(self.get_data(seq).iloc[0].to_list() + [seq])
        return pd.DataFrame(rows, columns=self.get_data(self.sequence[iloc]).columns.append(pd.Index([self.sequence_group])))

def make_whitespace_reader(col_names: Sequence = tuple()) -> DataReader:
    return partial(pd.read_csv, delim_whitespace=True, names=col_names if col_names else None) # type: ignore

def make_csv_reader(col_names: Sequence = tuple()) -> DataReader:
    return partial(pd.read_csv, names=col_names if col_names else None) # type: ignore

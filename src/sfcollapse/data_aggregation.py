from __future__ import annotations
from dataclasses import dataclass

from typing import TYPE_CHECKING, Iterable, Pattern

if TYPE_CHECKING:
    from pathlib import Path

@dataclass
class DataAggregator:
    _path: Path
    _pattern: Pattern

    @property
    def sources(self) -> Iterable:
        return sorted(p for p in self._path.iterdir() if self._pattern.search(p))

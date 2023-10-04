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
    def sources(self) -> Iterable[str]:
        return sorted(
            p.name for p in self._path.iterdir()
            if self._pattern.search(str(p))
        )

    @property
    def sequence(self, group=1) -> Iterable[float]:
        groups = (self._pattern.search(s) for s in self.sources)
        return [float(g.group(group)) for g in groups] # type: ignore

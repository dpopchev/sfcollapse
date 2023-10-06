from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Iterable, Match, Pattern, Protocol, Tuple, Union

if TYPE_CHECKING:
    from pathlib import Path

class Stringable(Protocol):
    def __str__(self) -> str:
        ...

@dataclass
class DataAggregator:
    _path: Path
    _pattern: Pattern
    group: int = 1

    def _make_match(self, text: Stringable) -> Union[Match, None]:
        return self._pattern.search(str(text))

    def _mask_sources(self) -> Iterable[Tuple[Path, Union[Match, None]]]:
        return [(p, self._make_match(p)) for p in self._path.iterdir()]

    def _get_sources(self) -> Dict[float, Path]:
        return dict((float(m.group(self.group)),p) for p, m in self._mask_sources() if m)

    @property
    def sources(self) -> Iterable[str]:
        return sorted(p.name for p in self._get_sources().values())

    @property
    def sequence(self) -> Iterable[float]:
        return sorted(s for s in self._get_sources().keys())

from collections import deque
from typing import Iterable, Iterator, Sized, TypeVar

from cytoolz.functoolz import do

from ftoolz.typing import Seq

_E = TypeVar('_E')
_T = TypeVar('_T')


class Ring(Iterator[_E], Sized):
    """Fixed-size in-memory rotating list of elements"""

    def __init__(self, elements: Iterable[_E] = tuple()) -> None:
        self._ring = deque(elements)

    def __len__(self) -> int:
        return len(self._ring)

    def __bool__(self) -> bool:
        return bool(self._ring)

    def __next__(self) -> _E:
        if not self:
            raise StopIteration
        return do(self._ring.append, self._ring.popleft())

    def state(self) -> Seq[_E]:
        return tuple(self._ring)

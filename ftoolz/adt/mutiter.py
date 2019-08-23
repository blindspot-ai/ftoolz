from collections import deque
from typing import Deque, Iterable, Iterator, Optional, Sized, TypeVar

from ftoolz.typing import Seq

_E = TypeVar('_E')


class MutIter(Iterator[_E], Sized):  # pylint: disable=E0239
    """
    Mutable iterator that can be both appended and consumend. Example usage is
    as an accumulator for `reduceby`.

    This implementation holds all data in memory. This means that the
    :class:`Iterable` of an initial state is fully consumed.

    **Warn**: This implementation is **not** thread-safe.

    Example behavior:

    >>> it = MutIter([1, 2])
    >>> print(it)
    MutIter(1, 2)

    >>> it += 3
    >>> print(it)
    MutIter(1, 2, 3)

    >>> it.state()
    (1, 2, 3)

    >>> next(it), next(it), next(it)
    (1, 2, 3)
    >>> next(it, -1)
    -1

    >>> MutIter.add(it, 42)
    MutIter(state=deque([42]))
    """

    def __init__(self, state: Optional[Iterable[_E]] = None) -> None:
        """
        >>> MutIter()
        MutIter(state=deque([]))
        >>> MutIter([1, 2, 3])
        MutIter(state=deque([1, 2, 3]))
        """
        super().__init__()
        self._state: Deque[_E] = deque(state) if state is not None else deque()

    @staticmethod
    def add(it: 'MutIter', e: _E) -> 'MutIter':
        """
        Binop which adds `e` to `it` state and returns modified state.

        >>> MutIter.add(MutIter([1, 2]), 3)
        MutIter(state=deque([1, 2, 3]))
        >>> MutIter.add(MutIter([]), 42)
        MutIter(state=deque([42]))
        """
        it += e
        return it

    def state(self) -> Seq[_E]:
        """
        Get immutable copy of current state.

        >>> MutIter([1, 2, 3]).state()
        (1, 2, 3)
        >>> MutIter().state()
        ()
        """
        return tuple(self._state)

    def __iadd__(self, other: _E) -> 'MutIter':
        """
        >>> it = MutIter()
        >>> it += 4
        >>> it += 2
        >>> it
        MutIter(state=deque([4, 2]))
        """
        self._state.append(other)
        return self

    def __iter__(self) -> 'MutIter':
        """
        >>> it = MutIter()
        >>> it is iter(it)
        True
        """
        return self

    def __next__(self) -> _E:
        """
        >>> next(MutIter())
        Traceback (most recent call last):
        ...
        StopIteration
        >>> next(MutIter(), None)
        >>> it = MutIter([1, 2, 3])
        >>> next(it)
        1
        >>> it
        MutIter(state=deque([2, 3]))
        """
        if not self._state:
            raise StopIteration
        return self._state.popleft()

    def __len__(self) -> int:
        """
        >>> len(MutIter([]))
        0
        >>> len(MutIter([1, 2, 3]))
        3
        """
        return len(self._state)

    def __bool__(self) -> bool:
        """
        >>> bool(MutIter())
        False
        >>> bool(MutIter([1, 2, 3]))
        True
        """
        return bool(self._state)

    def __repr__(self) -> str:
        return f'MutIter(state={repr(self._state)})'

    def __str__(self) -> str:
        return f'MutIter{self.state()}'

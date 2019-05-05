from typing import Iterable, Mapping, Optional, Sequence, TypeVar

A = TypeVar('A')
B = TypeVar('B')

Map = Mapping
Seq = Sequence


class TypingError(RuntimeError):
    pass


def assert_some(a: Optional[A]) -> A:
    """
    Assert given optional has some value or raise :class:`TypingError`.

    >>> assert_some('a')
    'a'
    >>> assert_some(None)
    Traceback (most recent call last):
    ...
    ftoolz.typing.TypingError: Item expected to be not None, None given.
    """
    if a is None:
        raise TypingError('Item expected to be not None, None given.')
    return a


def seq(it: Iterable[A] = ()) -> Seq[A]:
    """
    Type constructor for immutable :class:`Seq`.

    >>> it = iter([1, 2, 3])
    >>> seq(it)
    (1, 2, 3)

    Constructor is terminal in provided :class:`Iterable`.
    >>> next(it)
    Traceback (most recent call last):
    ...
    StopIteration

    >>> seq(iter([]))
    ()
    >>> seq()
    ()
    """
    return tuple(it)

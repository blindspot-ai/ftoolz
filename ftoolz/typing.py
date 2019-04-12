from typing import Mapping, Optional, Sequence, TypeVar

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

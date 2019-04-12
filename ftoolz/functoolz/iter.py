from itertools import starmap
from typing import Any, Callable, Iterable, Tuple

from cytoolz.itertoolz import identity, mapcat

from ftoolz.functoolz import A, A_in, A_out, B, B_in, B_out, C_out


def apply(
        ff: Iterable[Callable[[A_in], B_out]],
        fa: Iterable[A_in]
) -> Iterable[B_out]:
    """
    Given a value and a function in the :class:`Iterable` context,
    applies the function to the value.

    >>> f1 = lambda x: str(x + 1)
    >>> f2 = lambda x: str(x + 3)

    Result is empty if at least one of given iterables is empty.

    >>> list(apply(iter([]), iter([])))
    []
    >>> list(apply(iter([f1, f2]), iter([])))
    []
    >>> list(apply(iter([]), iter([1, 2])))
    []

    >>> list(apply(iter([f1]), iter([1, 2])))
    ['2', '3']

    >>> list(apply(iter([f1, f2]), iter([1])))
    ['2', '4']

    >>> ff = iter([f1, f2])
    >>> fa = iter([1, 2])
    >>> list(apply(ff, fa))
    ['2', '3', '4', '5']

    **Warn**: This operation is terminal in both given iterables and thus
    not a pure function.

    >>> next(ff)
    Traceback (most recent call last):
    ...
    StopIteration
    >>> next(fa)
    Traceback (most recent call last):
    ...
    StopIteration
    """
    fas = list(fa)
    return flatmap(lambda f: fmap(f, fas), ff)


flatmap = mapcat


def flatten(ffa: Iterable[Iterable[A]]) -> Iterable[A]:
    """
    Flatten a nested `Iterable` of `Iterable` structure into a single-layer
    `Iterable` structure.

    >>> list(flatten(iter([])))
    []

    >>> ffa = iter([[1], [2], [], [3, 4], []])
    >>> list(flatten(ffa))
    [1, 2, 3, 4]

    **Warn**: This operation is terminal in `ffa` and thus not a pure function.

    >>> next(ffa)
    Traceback (most recent call last):
    ...
    StopIteration
    """
    return flatmap(identity, ffa)


fmap = map


def fmap2(
        f: Callable[[A_in, B_in], C_out],
        fa: Iterable[A_in],
        fb: Iterable[B_in]
) -> Iterable[C_out]:
    """
    Bi-functor map for :class:`Iterable`.

    >>> def f(a: int, b: str) -> str:
    ...     return b * a

    Result is empty if at least one of given iterables is empty.

    >>> list(fmap2(f, iter([]), iter([])))
    []
    >>> list(fmap2(f, iter([1, 2, 3]), iter([])))
    []
    >>> list(fmap2(f, iter([]), iter(['a', 'b'])))
    []

    Input iterables do not have to be of equal size.

    >>> fa = iter([1, 2, 3])
    >>> fb = iter(['a', 'b'])
    >>> list(fmap2(f, fa, fb))
    ['a', 'b', 'aa', 'bb', 'aaa', 'bbb']

    **Warn**: This operation is terminal in both arguments and thus not a pure
    function.

    >>> next(fa)
    Traceback (most recent call last):
    ...
    StopIteration
    >>> next(fb)
    Traceback (most recent call last):
    ...
    StopIteration
    """
    fbs = list(fb)

    def ff(a: A_in) -> Iterable[C_out]:
        return fmap(lambda b: f(a, b), fbs)

    return flatmap(ff, fa)


def fproduct(
        f: Callable[[A], B_out],
        fa: Iterable[A]
) -> Iterable[Tuple[A, B_out]]:
    """
    Tuple the values in fa with the result of applying a function with
    the value.

    >>> def f(x: int) -> str:
    ...     return str(x)

    >>> list(fproduct(f, iter([])))
    []

    >>> fa = iter([1, 2, 3])
    >>> list(fproduct(f, fa))
    [(1, '1'), (2, '2'), (3, '3')]

    **Warn**: This operation is terminal in `fa` and thus not a pure function.

    >>> next(fa)
    Traceback (most recent call last):
    ...
    StopIteration
    """
    return fmap(lambda a: (a, f(a)), fa)


def lift(
        f: Callable[[A_in], B_out]
) -> Callable[[Iterable[A_in]], Iterable[B_out]]:
    """
    Lift a function f to operate on :class:`Iterable`.

    >>> def f(x: int) -> str:
    ...     return str(x)

    >>> lifted = lift(f)

    >>> list(lifted(iter([])))
    []

    >>> list(lifted(iter([1, 2, 3])))
    ['1', '2', '3']
    """
    return lambda fa: fmap(f, fa)


def product(fa: Iterable[A], fb: Iterable[B]) -> Iterable[Tuple[A, B]]:
    """
    Combine an `Iterable[A]` and an `Iterable[B]` into an `Iterable[(A, B)]`
    that maintains the effects of both `fa` and `fb`.

    Result is empty if at least one of given iterables is empty.

    >>> list(product(iter([]), iter([])))
    []
    >>> list(product(iter([1, 2, 3]), iter([])))
    []
    >>> list(product(iter([]), iter(['a', 'b'])))
    []

    Input iterables do not have to be of equal size.

    >>> fa = iter([1, 2, 3])
    >>> fb = iter(['a', 'b'])
    >>> list(product(fa, fb))
    [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b'), (3, 'a'), (3, 'b')]

    **Warn**: This operation is terminal in both arguments and thus not a pure
    function.

    >>> next(fa)
    Traceback (most recent call last):
    ...
    StopIteration
    >>> next(fb)
    Traceback (most recent call last):
    ...
    StopIteration
    """
    fbs = list(fb)

    # Because pylint does not allow `lambda a: fmap(lambda b: (a, b), fbs)`.
    def ff(a: A) -> Iterable[Tuple[A, B]]:
        return fmap(lambda b: (a, b), fbs)

    return flatmap(ff, fa)


def unit(a: A) -> Iterable[A]:
    """
    Unit value for :class:`Iterable`. Returns single item generator.

    >>> list(unit(42))
    [42]
    """
    yield a


def zip_map(f: Callable[..., A_out], *fx: Iterable[Any]) -> Iterable[A_out]:
    """
    >>> def f(a: int, b: str) -> str:
    ...     return b * a

    >>> list(zip_map(f, iter([]), iter([])))
    []
    >>> list(zip_map(f, iter([1, 2, 3]), iter([])))
    []
    >>> list(zip_map(f, iter([]), iter(['a', 'b'])))
    []

    >>> fa = iter([1, 2, 3, 4])
    >>> fb = iter(['a', 'b', 'c'])
    >>> list(zip_map(f, fa, fb))
    ['a', 'bb', 'ccc']

    **Warn**: This operation is terminal in all given iterables and thus
    not a pure function.

    >>> next(fa)
    Traceback (most recent call last):
    ...
    StopIteration
    >>> next(fb)
    Traceback (most recent call last):
    ...
    StopIteration
    """
    return starmap(f, zip(*fx))

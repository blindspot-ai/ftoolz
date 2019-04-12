from itertools import starmap
from typing import Any, Callable, Tuple

from cytoolz.itertoolz import identity, mapcat

from ftoolz.functoolz import A, A_in, A_out, B, B_in, B_out, C_out
from ftoolz.typing import Seq


def apply(ff: Seq[Callable[[A_in], B_out]], fa: Seq[A_in]) -> Seq[B_out]:
    """
    Given a value and a function in the :class:`Seq` context,
    applies the function to the value.

    >>> f1 = lambda x: str(x + 1)
    >>> f2 = lambda x: str(x + 3)

    Result is empty if at least one of given iterables is empty.

    >>> apply(tuple(), tuple())
    ()
    >>> apply((f1, f2), tuple())
    ()
    >>> apply(tuple(), (1, 2))
    ()

    >>> apply((f1,), (1, 2))
    ('2', '3')

    >>> apply((f1, f2), (1,))
    ('2', '4')

    >>> apply((f1, f2), (1, 2))
    ('2', '3', '4', '5')
    """
    return flatmap(lambda f: fmap(f, fa), ff)


def flatmap(f: Callable[[A_in], Seq[B_out]], fa: Seq[A_in]) -> Seq[B_out]:
    """
    Feed value in context `(Seq[A])` into a function that takes a normal
    value and returns a value in a context `(A -> Seq[B])`.

    >>> def f(x: int) -> Seq[str]:
    ...     return str(x), str(x)

    >>> flatmap(f, tuple())
    ()
    >>> flatmap(f, (1, 2, 3))
    ('1', '1', '2', '2', '3', '3')
    """
    return tuple(mapcat(f, fa))


def flatten(ffa: Seq[Seq[A]]) -> Seq[A]:
    """
    Flatten a nested `Seq` of `Seq` structure into a single-layer
    `Seq` structure.

    >>> flatten((tuple(), tuple()))
    ()
    >>> flatten(((1,), (2,), tuple(), (3, 4), tuple()))
    (1, 2, 3, 4)
    """
    return flatmap(identity, ffa)


def fmap(f: Callable[[A_in], B_out], fa: Seq[A_in]) -> Seq[B_out]:
    """
    Functor map for :class:`Seq`.

    >>> def f(x: int) -> str:
    ...     return str(x)

    >>> fmap(f, tuple())
    ()
    >>> fmap(f, (1, 2, 3))
    ('1', '2', '3')
    """
    return tuple(f(a) for a in fa)


def fmap2(
        f: Callable[[A_in, B_in], C_out],
        fa: Seq[A_in],
        fb: Seq[B_in]
) -> Seq[C_out]:
    """
    Bi-functor map for :class:`Seq`.

    >>> def f(a: int, b: str) -> str:
    ...     return b * a

    Result is empty if at least one of given sequences is empty.

    >>> fmap2(f, tuple(), tuple())
    ()
    >>> fmap2(f, (1, 2), tuple())
    ()
    >>> fmap2(f, tuple(), ('a', 'b'))
    ()

    Input sequences do not have to be of equal size.

    >>> fmap2(f, (1, 2, 3), ('a', 'b'))
    ('a', 'b', 'aa', 'bb', 'aaa', 'bbb')
    """

    def ff(a: A_in) -> Seq[C_out]:
        return fmap(lambda b: f(a, b), fb)

    return tuple() if not fb else flatmap(ff, fa)


def fproduct(f: Callable[[A], B_out], fa: Seq[A]) -> Seq[Tuple[A, B_out]]:
    """
    Tuple the values in fa with the result of applying a function with
    the value.

    >>> def f(x: int) -> str:
    ...     return str(x)

    >>> fproduct(f, tuple())
    ()
    >>> fproduct(f, (1, 2, 3))
    ((1, '1'), (2, '2'), (3, '3'))
    """
    return fmap(lambda a: (a, f(a)), fa)


def lift(f: Callable[[A_in], B_out]) -> Callable[[Seq[A_in]], Seq[B_out]]:
    """
    Lift a function f to operate on :class:`Seq`.

    >>> def f(x: int) -> str:
    ...     return str(x)

    >>> lifted = lift(f)

    >>> lifted(tuple())
    ()
    >>> lifted((1, 2, 3))
    ('1', '2', '3')
    """
    return lambda fa: fmap(f, fa)


def product(fa: Seq[A], fb: Seq[B]) -> Seq[Tuple[A, B]]:
    """
    Combine an `Seq[A]` and an `Seq[B]` into an `Seq[(A, B)]`
    that maintains the effects of both `fa` and `fb`.

    Result is empty if at least one of given sequences is empty.

    >>> product(tuple(), tuple())
    ()
    >>> product((1, 2, 3), tuple())
    ()
    >>> product(tuple(), ('a', 'b'))
    ()

    Input sequences do not have to be of equal size.

    >>> product((1, 2, 3), ('a', 'b'))
    ((1, 'a'), (1, 'b'), (2, 'a'), (2, 'b'), (3, 'a'), (3, 'b'))
    """

    # Because pylint does not allow `lambda a: fmap(lambda b: (a, b), fbs)`.
    def ff(a: A) -> Seq[Tuple[A, B]]:
        return fmap(lambda b: (a, b), fb)

    return flatmap(ff, fa)


def unit(a: A) -> Seq[A]:
    """
    Unit value for :class:`Seq`. Returns 1-tuple.

    >>> unit(42)
    (42,)
    """
    return a,


def zip_map(f: Callable[..., A_out], *fx: Seq[Any]) -> Seq[A_out]:
    """
    >>> def f(a: int, b: str) -> str:
    ...     return b * a

    Result is empty if at least one of given sequences is empty.

    >>> zip_map(f, tuple(), tuple())
    ()
    >>> zip_map(f, (1, 2, 3), tuple())
    ()
    >>> zip_map(f, tuple(), ('a', 'b'))
    ()

    Input sequences do not have to be of equal size.

    >>> zip_map(f, (1, 2, 3, 4), ('a', 'b', 'c'))
    ('a', 'bb', 'ccc')
    """
    return tuple(starmap(f, zip(*fx)))

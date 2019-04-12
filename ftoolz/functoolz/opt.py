from typing import Any, Callable, Optional, Tuple

from ftoolz.functoolz import A, A_in, A_out, B, B_in, B_out, C_in, C_out, \
    D_out


def apply(
        ff: Optional[Callable[[A_in], B_out]],
        fa: Optional[A_in]
) -> Optional[B_out]:
    """
    Given a value and a function in the :class:`Optional` context,
    applies the function to the value.

    >>> ff = lambda x: str(x)
    >>> apply(ff, None)
    >>> apply(None, 42)
    >>> apply(None, None)
    >>> apply(ff, 42)
    '42'
    """
    if ff is not None and fa is not None:
        return ff(fa)
    return None


def apply2(
        ff: Optional[Callable[[A_in, B_in], C_out]],
        fa: Optional[A_in],
        fb: Optional[B_in]
) -> Optional[C_out]:
    """
    Given two values and a function in the :class:`Optional` context,
    applies the function to the values.

    >>> ff = lambda x, y: f'{x}{y}'
    >>> apply2(ff, None, None)
    >>> apply2(None, 4, None)
    >>> apply2(None, None, '2')
    >>> apply2(None, None, None)
    >>> apply2(None, 4, '2')
    >>> apply2(ff, 4, '2')
    '42'
    """
    if ff is not None and fa is not None and fb is not None:
        return ff(fa, fb)
    return None


def applyN(
        ff: Optional[Callable[..., A_out]],
        *fx: Optional[Any]
) -> Optional[A_out]:
    """
    Given N values and a function in the :class:`Optional` context,
    applies the function to the values.

    >>> ff = lambda x, y: f'{x}{y}'
    >>> applyN(ff, None, None)
    >>> applyN(None, 4, None)
    >>> applyN(None, None, '2')
    >>> applyN(None, None, None)
    >>> applyN(None, 4, '2')
    >>> applyN(ff, 4, '2')
    '42'

    **Warn**: For static type-safety, prefer :ref:`apply`, :ref:`apply2`,
    this function may raise runtime errors.

    >>> applyN(lambda x, y: x + y, 1, '2')
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type(s) for +: 'int' and 'str'

    >>> applyN(ff, 4, '2', 'fail')
    Traceback (most recent call last):
    ...
    TypeError: <lambda>() takes 2 positional arguments but 3 were given
    """
    if ff is not None and all(x is not None for x in fx):
        return ff(*fx)
    return None


def flatmap(
        f: Callable[[A_in], Optional[B_out]],
        fa: Optional[A_in]
) -> Optional[B_out]:
    """
    Feed value in context `(Optional[A_contra])` into a function that takes a
    normal value and returns a value in a context
    `(A_contra -> Optional[B_co])`.

    >>> def test_func(x: int) -> Optional[str]:
    ...     return str(100 // x) if x != 0 else None

    >>> flatmap(test_func, None)

    >>> flatmap(test_func, 42)
    '2'

    >>> flatmap(test_func, 0)
    """
    return None if fa is None else f(fa)


def flatten(ffa: Optional[Optional[A]]) -> Optional[A]:
    """
    Flatten double :class:`Optional` context into single one.

    >>> flatten(None)
    >>> flatten(42)
    42
    """
    return None if ffa is None else ffa


def fmap(
        f: Callable[[A_in], B_out],
        fa: Optional[A_in]
) -> Optional[B_out]:
    """
    Functor map for :class:`Optional`.

    >>> add_one = lambda x: str(x + 1)
    >>> one: Optional[int] = 1

    >>> fmap(add_one, one)
    '2'
    >>> fmap(add_one, None)
    """
    return f(fa) if fa is not None else None


def fmap2(
        f: Callable[[A_in, B_in], C_out],
        fa: Optional[A_in],
        fb: Optional[B_in]
) -> Optional[C_out]:
    """
    Bi-functor map for :class:`Optional`.

    >>> def f(a: int, b: str) -> Optional[str]:
    ...     return str(a) if b == 'x' else None

    >>> fmap2(f, None, None)
    >>> fmap2(f, None, '2')
    >>> fmap2(f, 1, None)
    >>> fmap2(f, 1, '2')
    >>> fmap2(f, 42, 'x')
    '42'
    """

    def ff(a: A_in) -> Optional[C_out]:
        return fmap(lambda b: f(a, b), fb)

    return flatmap(ff, fa)


def fmap3(
        f: Callable[[A_in, B_in, C_in], D_out],
        fa: Optional[A_in],
        fb: Optional[B_in],
        fc: Optional[C_in],
) -> Optional[D_out]:
    """
    3-functor map for :class:`Optional`.

    >>> def f(a: int, b: str, c: str) -> Optional[str]:
    ...     return str(a) if b == 'x' and c == 'y' else None

    >>> fmap3(f, None, None, None)
    >>> fmap3(f, 1, None, None)
    >>> fmap3(f, None, '2', None)
    >>> fmap3(f, None, None, '3')
    >>> fmap3(f, 1, '2', None)
    >>> fmap3(f, 1, None, '3')
    >>> fmap3(f, 1, 'x', 'z')
    >>> fmap3(f, 42, 'x', 'y')
    '42'
    """

    def ff(a: A_in) -> Optional[D_out]:
        return fmap2(lambda b, c: f(a, b, c), fb, fc)

    return flatmap(ff, fa)


def fmapN(f: Callable[..., A_out], *fx: Optional[Any]) -> Optional[A_out]:
    """
    Generic N-functor map for :class:`Optional`.

    >>> def f(x: int, y: str) -> str:
    ...     return f'{x}{y}'

    >>> fmapN(f, None, None)
    >>> fmapN(f, 1, None)
    >>> fmapN(f, None, '2')
    >>> fmapN(f, 4, '2')
    '42'

    **Warn**: For static type-safety, prefer :ref:`fmap`, :ref:`fmap2` and
    :ref:`fmap3`, this function may raise runtime errors.

    >>> fmapN(lambda x, y: x + y, 1, '2')
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type(s) for +: 'int' and 'str'

    >>> fmapN(f, 4, '2', 'fail')
    Traceback (most recent call last):
    ...
    TypeError: f() takes 2 positional arguments but 3 were given
    """
    return None if any(x is None for x in fx) else f(*fx)


def fproduct(
        f: Callable[[A], B_out],
        fa: Optional[A]
) -> Optional[Tuple[A, B_out]]:
    """
    Tuple the values in fa with the result of applying a function with
    the value.

    >>> def f(x: int) -> str:
    ...     return str(x)

    >>> fproduct(f, 42)
    (42, '42')
    >>> fproduct(f, None)
    """
    return fmap(lambda a: (a, f(a)), fa)


def lift(
        f: Callable[[A_in], B_out]
) -> Callable[[Optional[A_in]], Optional[B_out]]:
    """
    Lift a function f to operate on :class:`Optional`.

    >>> def f(x: int) -> str:
    ...     return str(x)

    >>> lifted = lift(f)

    >>> lifted(None)
    >>> lifted(42)
    '42'
    """
    return lambda fa: fmap(f, fa)


def product(fa: Optional[A], fb: Optional[B]) -> Optional[Tuple[A, B]]:
    """
    Combine an `Optional[A]` and an `Optional[B]` into an `Optional[(A, B)]`
    that maintains the effects of both `fa` and `fb`.

    >>> product(None, None)
    >>> product(1, None)
    >>> product(None, '2')
    >>> product(4, '2')
    (4, '2')
    """

    # Because pylint does not allow `lambda a: map_opt(lambda b: (a, b), fb)`.
    def ff(a: A) -> Optional[Tuple[A, B]]:
        return fmap(lambda b: (a, b), fb)

    return flatmap(ff, fa)

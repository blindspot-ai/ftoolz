import functools
from typing import Any, Callable, Optional, Tuple, Type, TypeVar, Union

from cytoolz import compose

from ftoolz.typing import Map

# Invariant
A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
D = TypeVar('D')

# Contravariant
A_in = TypeVar('A_in', contravariant=True)
B_in = TypeVar('B_in', contravariant=True)
C_in = TypeVar('C_in', contravariant=True)
D_in = TypeVar('D_in', contravariant=True)

# Covariant
A_out = TypeVar('A_out', covariant=True)
B_out = TypeVar('B_out', covariant=True)
C_out = TypeVar('C_out', covariant=True)
D_out = TypeVar('D_out', covariant=True)


def attempt(
        e: Union[Type[Exception], Tuple[Type[Exception], ...]],
        f: Callable[..., A],
        *args: Any,
        **kwargs: Any
) -> Optional[A]:
    """
    Attempt to return `f(args, kwargs)` and on errors `e` fallback to `None`.

    >>> attempt(ValueError, int, '1')
    1
    >>> attempt(ValueError, int, 'a')

    One can pass both args and kwargs to `f` via `attempt`.

    >>> def f(x: int, y: str) -> int:
    ...     return x + int(y)

    >>> attempt(ValueError, f, 1, y='2')
    3
    >>> attempt(ValueError, f, 1, y='x')

    Errors that are not mentioned in `e` are propagated to outer scope.

    >>> attempt(ValueError, lambda d: d['k'], {'a': 1})
    Traceback (most recent call last):
    ...
    KeyError: 'k'
    """

    def none(*_args: Any, **_kwargs: Any) -> Optional[A]:
        return None

    return try_except(e, f, none, *args, **kwargs)


def chain(*fs: Callable) -> Callable:
    """
    Compose given functions in reversed order.

    Given functions f, g, the result of chain is chain(f, g) = g o f.

    >>> def f(x: int) -> int:
    ...     return x + 1

    >>> def g(x: int) -> str:
    ...     return str(x)

    >>> chain(f, g)(41)
    '42'

    Chaining single function is the function itself.

    >>> chain(f) is f
    True

    Empty function chain is identity.

    >>> chain()(42)
    42
    """
    g: Callable = compose(*reversed(fs))
    return g


def silenced(
        _f: Optional[Callable[..., A]] = None,
        *,
        error: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception
) -> Callable[[Callable[..., A]], Callable[..., Optional[A]]]:
    """
    Decorator that turns `errors` raised by decorated function into `None`.

    >>> @silenced(error=ValueError)
    ... def f(x: int, y: str) -> int:
    ...     return x + int(y)

    >>> f(1, y='2')
    3

    >>> f(1, y='x')

    Errors that are not mentioned in `error` are propagated to outer scope.

    >>> @silenced(error=ValueError)
    ... def g(d: Map[str, Any]) -> Any:
    ...     return d['k']

    >>> g({'a': 1})
    Traceback (most recent call last):
    ...
    KeyError: 'k'

    By default any `Exception` is silenced.

    >>> @silenced
    ... def h(d: Map[str, Any]) -> Any:
    ...     return d['k']

    >>> h({'a': 42})
    """

    def decorator(f: Callable[..., A]) -> Callable[..., Optional[A]]:
        @functools.wraps(f)
        def wrapper(*args: Any, **kwargs: Any) -> Optional[A]:
            return attempt(error, f, *args, **kwargs)

        return wrapper

    return decorator if _f is None else decorator(_f)  # type: ignore


def try_apply(f: Callable[..., A], *args: Any, **kwargs: Any) -> Optional[A]:
    """
    Run `f(args, kwargs)` and on **any** error fallback to `None`.

    >>> def f(x: int, y: str) -> int:
    ...     return x + int(y)

    >>> try_apply(f, 1, y='2')
    3
    >>> try_apply(f, 1, y='x')
    >>> try_apply(lambda d: d['k'], {'a': 1})
    """
    return attempt(Exception, f, *args, **kwargs)


def try_except(
        e: Union[Type[Exception], Tuple[Type[Exception], ...]],
        f: Callable[..., A],
        g: Callable[..., A],
        *args: Any,
        **kwargs: Any
) -> A:
    """
    Call `f(args, kwargs)` and on exception `e` fallback to `g(args, kwargs)`.

    >>> try_except(ValueError, int, lambda s: s.upper(), '1')
    1
    >>> try_except(ValueError, int, lambda s: s.upper(), 'a')
    'A'

    One can pass both args and kwargs to `try_except`.

    >>> def f(x: int, y: str):
    ...     return x + int(y)

    >>> def g(x: int, y: str):
    ...     return f'error: {x} + {y}'

    >>> try_except(ValueError, f, g, 1, y='2')
    3

    >>> try_except(ValueError, f, g, 1, y='x')
    'error: 1 + x'

    Errors that are not mentioned in `e` are propagated to outer scope.

    >>> try_except(ValueError, lambda d: d['k'], str, {'a': 1})
    Traceback (most recent call last):
    ...
    KeyError: 'k'
    """
    # noinspection PyBroadException
    try:
        return f(*args, **kwargs)
    except e:
        return g(*args, **kwargs)

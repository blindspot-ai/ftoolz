from typing import Callable, Iterable, Optional

from cytoolz.itertoolz import cons, identity

from ftoolz.functoolz import A, A_in, B
from ftoolz.functoolz.opt import fmap, fmap2
from ftoolz.itertoolz import fold_right
from ftoolz.typing import Seq


def sequence_iter(gfa: Iterable[Optional[A]]) -> Optional[Iterable[A]]:
    """
    Thread all the `Optional` effects through the `Iterable` structure.

    >>> from typing import NamedTuple
    >>> class Foo(NamedTuple):
    ...     bar: int

    >>> gfa = iter([Foo(1), Foo(2), Foo(3)])

    >>> tuple(sequence_iter(gfa))
    (Foo(bar=1), Foo(bar=2), Foo(bar=3))

    **Warn**: This operation is terminal in input argument and thus not a pure
    function.

    >>> next(gfa)
    Traceback (most recent call last):
    ...
    StopIteration

    >>> sequence_iter(iter([Foo(1), None, Foo(3)]))

    >>> tuple(sequence_iter(iter([])))
    ()

    """
    return traverse_iter(identity, gfa)


def sequence_seq(gfa: Seq[Optional[A]]) -> Optional[Seq[A]]:
    """
    Thread all the `Optional` effects through the `Seq` structure.

    >>> from typing import NamedTuple
    >>> class Foo(NamedTuple):
    ...     bar: int

    >>> sequence_seq((Foo(1), Foo(2), Foo(3)))
    (Foo(bar=1), Foo(bar=2), Foo(bar=3))

    >>> sequence_seq((Foo(1), None, Foo(3)))

    >>> sequence_seq(tuple())
    ()
    """
    return fmap(tuple, traverse_iter(identity, gfa))


def traverse_iter(
        f: Callable[[A_in], Optional[B]],
        seq: Iterable[A_in]
) -> Optional[Iterable[B]]:
    """
    Given a function which returns a `Optional` effect, thread this effect
    through the running of this function on all the values in `Iterable`,
    returning an `Iterable[B]` in a `Optional` context.

    **Warn**: This operation is terminal in input iterable and thus not a pure
    function.
    """

    def op(a: A_in, acc: Optional[Iterable[B]]) -> Optional[Iterable[B]]:
        # FIXME: mypy cannot resolve correct type event though it's fine
        op_res: Optional[Iterable[B]] = fmap2(cons, f(a), acc)
        return op_res

    empty: Optional[Iterable[B]] = iter([])
    return fold_right(op, seq, empty)


def traverse_seq(
        f: Callable[[A_in], Optional[B]],
        fa: Seq[A_in]
) -> Optional[Seq[B]]:
    """
    Given a function which returns a `Optional` effect, thread this effect
    through the running of this function on all the values in `Seq`,
    returning an `Seq[B]` in a `Optional` context.

    >>> def f(x: int) -> Optional[str]:
    ...     return str(x) if x > 0 else None

    >>> traverse_seq(f, (1, 2, 3))
    ('1', '2', '3')

    >>> traverse_seq(f, (0, 1, 2))

    >>> traverse_seq(f, tuple())
    ()
    """
    return fmap(tuple, traverse_iter(f, fa))

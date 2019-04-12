from functools import reduce
from itertools import islice
from typing import Callable, Iterable, List, Optional, Reversible, Tuple, \
    TypeVar

from cytoolz.functoolz import complement, compose
from cytoolz.itertoolz import drop, identity, last as clast, peek, unique

from ftoolz.typing import Map, Seq

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
E = TypeVar('E')


def associate(key: Callable[[B], A], values: Iterable[B]) -> Map[A, B]:
    """
    Collect values into a :class:`Map` using provided key function.

    >>> key = lambda x: x[0]

    >>> associate(key, iter([]))
    {}

    >>> values = iter([('a', 1), ('b', 2), ('c', 3)])
    >>> associate(key, values)
    {'a': ('a', 1), 'b': ('b', 2), 'c': ('c', 3)}

    This operation is terminal in values.

    >>> next(values)
    Traceback (most recent call last):
    ...
    StopIteration

    Values are assumed to be unique with respect to the keys. Latter value is
    kept on key collision.

    >>> values = iter([('a', 1), ('a', 2)])
    >>> associate(key, values)
    {'a': ('a', 2)}
    """
    return associate_to(key, identity, values)


def associate_to(
        key: Callable[[B], A],
        value: Callable[[B], C],
        values: Iterable[B]
) -> Map[A, C]:
    """
    Collect values into a Map using provided key_func and value_func.

    >>> key = lambda x: x[0]
    >>> value = lambda x: x[1]

    >>> associate_to(key, value, iter([]))
    {}

    >>> values = iter([('a', 1), ('b', 2), ('c', 3)])
    >>> associate_to(key, value, values)
    {'a': 1, 'b': 2, 'c': 3}

    This operation is terminal in values.

    >>> next(values)
    Traceback (most recent call last):
    ...
    StopIteration

    Values are assumed to be unique with respect to the keys. Latter value is
    kept on key collision.

    >>> values = iter([('a', 1), ('a', 2)])
    >>> associate_to(key, value, values)
    {'a': 2}
    """
    return {key(v): value(v) for v in values}


def collect(items: Iterable[E]) -> Seq[E]:
    """
    Collect given `items` into a sequence (list). If the input iterable already
    is a sequence, it is just returned. Otherwise it is materialized.

    >>> it = iter([1, 2, 3])
    >>> collect(it)
    [1, 2, 3]

    This operation is terminal.

    >>> next(it)
    Traceback (most recent call last):
    ...
    StopIteration

    >>> in_seq = [1, 2, 3]
    >>> out_seq = collect(in_seq)
    >>> out_seq is in_seq
    True
    """
    return items if isinstance(items, Seq) else list(items)


def empty(it: Iterable[E]) -> Tuple[bool, Iterable[E]]:
    """
    Checks, whether the sequence is empty or not.

    NOTE: This method modifies the original sequence (takes the first element),
    use the returned one, which contains the original items.

    >>> it_orig = iter([1, 2, 3])
    >>> is_empty, it_new = empty(it_orig)
    >>> is_empty, list(it_new)
    (False, [1, 2, 3])

    >>> is_empty, it_empty = empty(iter([]))
    >>> is_empty, list(it_empty)
    (True, [])
    """
    try:
        _, it = peek(it)
        return False, it
    except StopIteration:
        return True, iter([])


def enumerate_with_final(it: Iterable[E]) -> Iterable[Tuple[E, bool, int]]:
    """
    Change given iterator to new one yielding additional *final* flag and
    iteration order.

    >>> list(enumerate_with_final(iter(['a', 'b', 'c'])))
    [('a', False, 0), ('b', False, 1), ('c', True, 2)]

    >>> list(enumerate_with_final(iter(['a'])))
    [('a', True, 0)]

    >>> list(enumerate_with_final(iter([])))
    []
    """
    it_final = iter_with_final(it)
    for i, (item, final) in enumerate(it_final):
        yield item, final, i


def filter_not_none(it: Iterable[Optional[E]]) -> Iterable[E]:
    """
    Filter items of given iterable which are not `None`, inferring non-optional
    return type `E`.

    >>> list(filter_not_none(iter([1, None, 3])))
    [1, 3]

    >>> list(filter_not_none([]))
    []

    >>> list(filter_not_none([None, None, None]))
    []
    """
    for e in it:
        if e is not None:
            yield e


def find(pred: Callable[[E], bool], it: Iterable[E]) -> Optional[E]:
    """
    Find first item from give iterable that satisfies `predicate`.

    >>> even = lambda x: x % 2 == 0
    >>> find(even, iter([1, 5, 4, 7, 2]))
    4
    >>> find(even, iter([1, 3, 5]))
    >>> find(even, iter([]))

    This operation is terminal in provided iterable.

    >>> it = iter([1, 2])
    >>> find(even, it)
    2
    >>> next(it)
    Traceback (most recent call last):
    ...
    StopIteration
    """
    return try_take_first(e for e in it if pred(e))


def first(seq: Seq[E]) -> Optional[E]:
    """
    Return first element of a sequence or `None` if empty.

    >>> first([1, 2, 3])
    1
    >>> first([])
    """
    return seq[0] if seq else None


def fold_right(op: Callable[[A, B], B], xs: Iterable[A], z: B) -> B:
    """
    Fold iterable `xs` by applying binary operator `op` from the *right* with
    `z` being initial value.

    >>> def op(a: int, b: str) -> str:
    ...     return f'{b} then {a}'

    >>> xs = iter([1, 2, 3])
    >>> fold_right(op, xs, '4')
    '4 then 3 then 2 then 1'

    This operation is terminal in `xs`.

    >>> next(xs)
    Traceback (most recent call last):
    ...
    StopIteration

    Initial value is returned given an empty iterable.

    >>> fold_right(op, iter([]), '42')
    '42'
    """
    seq: Reversible[A] = xs if isinstance(xs, Reversible) else list(xs)
    return reduce(lambda right, left: op(left, right), reversed(seq), z)


def head_tail(it: Iterable[E]) -> Tuple[E, Iterable[E]]:
    """
    Split provided iterable into head element and tail iterable.

    >>> head, tail = head_tail(iter([1, 2, 3]))
    >>> head, list(tail)
    (1, [2, 3])

    >>> head, tail = head_tail(iter([42]))
    >>> head, list(tail)
    (42, [])

    Raises :class:`StopIteration` if the original iterable is empty.

    >>> head_tail(iter([]))
    Traceback (most recent call last):
    ...
    StopIteration
    """
    head, seq = peek(it)
    tail = drop(1, seq)
    return head, tail


def head_tail_list(it: Iterable[E]) -> Tuple[E, List[E]]:
    """
    Split given iterable into head and tail :class:`List`.

    >>> head_tail_list(iter([1, 2, 3]))
    (1, [2, 3])

    >>> head_tail_list(iter([42]))
    (42, [])

    >>> head_tail_list(iter([]))
    Traceback (most recent call last):
    ...
    StopIteration
    """
    head, tail = head_tail(it)
    return head, list(tail)


def iter_with_final(it: Iterable[E]) -> Iterable[Tuple[E, bool]]:
    """
    Change given iterator to new one yielding additional *final* flag.

    >>> list(iter_with_final(iter([1, 2, 3])))
    [(1, False), (2, False), (3, True)]

    >>> list(iter_with_final(iter([42])))
    [(42, True)]

    >>> list(iter_with_final(iter([])))
    []
    """

    is_empty, iterable = empty(it)
    if is_empty:
        return iter([])

    it = iter(iterable)
    buffer = [next(it)]
    for i in it:
        buffer.append(i)
        item, buffer = head_tail_list(buffer)
        yield item, False
    yield buffer[0], True


def last(seq: Seq[E]) -> Optional[E]:
    """
    Return last element of a sequence or `None` if empty.

    >>> last([1, 2, 3])
    3
    >>> last([])
    """
    return seq[-1] if seq else None


def make_str(
        it: Iterable[E],
        key: Callable[[E], str] = str,
        sep: str = ','
) -> str:
    """
    Serialize objects selected by key from iterable to a string using separator

    >>> make_str(iter([1, 2, 3]))
    '1,2,3'
    >>> make_str(iter([]))
    ''
    >>> make_str(iter([1, 2, 3]), sep='; ')
    '1; 2; 3'

    >>> it = iter([{'k': 'a', 'v': 1}, {'k': 'b', 'v': 2}, {'k': 'c', 'v': 3}])
    >>> make_str(it, key=lambda x: x['k'], sep='-')
    'a-b-c'

    This operation is terminal in the iterable.

    >>> next(it)
    Traceback (most recent call last):
    ...
    StopIteration
    """
    tokens = map(key, it)
    return sep.join(tokens)


def split_by(
        pred: Callable[[E], bool],
        it: Iterable[E]
) -> Tuple[Iterable[E], Iterable[E]]:
    """
    Split given items by a predicate into (positives, negatives).

    >>> even = lambda x: x % 2 == 0
    >>> pos, neg = split_by(even, iter([1, 5, 4, 7, 2]))
    >>> list(pos), list(neg)
    ([4, 2], [1, 5, 7])

    >>> pos, neg = split_by(even, iter([1, 3, 5]))
    >>> list(pos), list(neg)
    ([], [1, 3, 5])

    >>> pos, neg = split_by(even, iter([]))
    >>> list(pos), list(neg)
    ([], [])

    This operation is terminal in given iterable.

    >>> it = iter([1, 2, 3])
    >>> _ = split_by(even, it)
    >>> next(it)
    Traceback (most recent call last):
    ...
    StopIteration
    """
    items = collect(it)
    rest = complement(pred)
    return filter(pred, items), filter(rest, items)


def take(n: int, it: Iterable[E]) -> Seq[E]:
    """
    Return first n items of the iterable as a list.

    >>> it = iter([1, 2, 3])
    >>> take(2, it)
    [1, 2]
    >>> next(it)
    3
    >>> take(2, it)
    []

    >>> take(0, [1, 2, 3])
    []

    >>> take(-1, [])
    Traceback (most recent call last):
    ...
    ValueError: n must be non-negative integer
    """
    if n < 0:
        raise ValueError('n must be non-negative integer')
    return list(islice(it, n))


def take_first(it: Iterable[E]) -> E:
    """
    Return the first item of the iterable or raise StopIteration if empty.

    >>> it = iter([1, 2])
    >>> take_first(it)
    1
    >>> next(it)
    2
    >>> take_first(it)
    Traceback (most recent call last):
    ...
    StopIteration
    """
    return next(iter(it))


def try_take_first(it: Iterable[E]) -> Optional[E]:
    """
    Return the first item of the iterable or None if empty.

    >>> it = iter([1, 2, 3])
    >>> try_take_first(it)
    1

    This operation does not change given iterable.

    >>> next(it)
    2

    >>> try_take_first(iter([]))
    """
    return next(iter(it), None)


def try_take_last(seq: Iterable[E]) -> Optional[E]:
    """
    Get last element of given sequence or return `None`.

    >>> it = iter([1, 2, 3])
    >>> try_take_last(it)
    3

    This operation is terminal.

    >>> try_take_last(it)
    """
    try:
        return clast(seq)
    except IndexError:
        return None


# Common composition of extracting unique items followed by list
unique_list: Callable[[Iterable[E]], Seq[E]] = compose(collect, unique)

# Common composition of extracting unique items followed by natural sort
unique_sorted: Callable[[Iterable[E]], Seq[E]] = compose(sorted, unique)

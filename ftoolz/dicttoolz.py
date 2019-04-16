from typing import Any, Callable, TypeVar

from cytoolz import assoc
from ftoolz.typing import Map

K = TypeVar('K')
V = TypeVar('V')


def map_val(d: Map[K, Any], key: K, f: Callable[[Any], Any]) -> Map[K, Any]:
    """
    Apply value transformation `f` on value in `d` under `key`.

    >>> map_val({'a': 1}, 'a', str)
    {'a': '1'}

    Returns original map if `key` does not exist in `d`. For different
    behavior use related function `update_in` from `cytoolz`.

    >>> map_val({'a': 1}, 'b', str)
    {'a': 1}
    """
    return assoc(d, key, f(d[key])) if key in d else d


def swap(d: Map[K, Any], key1: K, key2: K) -> Map[K, Any]:
    """
    Swap arbitrary values for given keys creating new mapping.

    >>> swap({'k1': [1, 2, 3], 'k2': {1, 2, 3}}, 'k1', 'k2')
    {'k1': {1, 2, 3}, 'k2': [1, 2, 3]}

    Original mapping is returned if at least one key does not exist in `d`.

    >>> swap({'k1': 1}, 'k1', 'k2')
    {'k1': 1}
    >>> swap({'k2': 2}, 'k1', 'k2')
    {'k2': 2}
    """
    return swap_values(d, key1, key2)


def swap_values(d: Map[K, V], key1: K, key2: K) -> Map[K, V]:
    """
    Swap values for given keys creating new mapping.

    >>> swap_values({'k1': 1, 'k2': 2}, 'k1', 'k2')
    {'k1': 2, 'k2': 1}

    Original mapping is returned if at least one key does not exist in `d`.

    >>> swap_values({'k1': 1}, 'k1', 'k2')
    {'k1': 1}
    >>> swap_values({'k2': 2}, 'k1', 'k2')
    {'k2': 2}
    """
    return {**d, key1: d[key2], key2: d[key1]} \
        if key1 in d and key2 in d \
        else d

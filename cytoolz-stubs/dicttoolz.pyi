from typing import Any, Callable, Dict, Mapping, Sequence, Tuple, TypeVar, \
    Union, overload

_K = TypeVar('_K')
_K1 = TypeVar('_K1')
_V = TypeVar('_V')
_V1 = TypeVar('_V1')


def assoc(
        d: Mapping[_K, _V],
        key: _K1,
        value: _V1,
        factory: Callable[[], Dict[Union[_K, _K1], Union[_V, _V1]]] = dict
) -> Dict[Union[_K, _K1], Union[_V, _V1]]: ...


def assoc_in(
        d: Mapping[_K, _V],
        keys: Sequence[Any],
        value: Any,
        factory: Callable[[], Dict[_K, Any]] = dict
) -> Dict[_K, Any]: ...


def dissoc(
        d: Mapping[_K, _V],
        *keys: _K,
) -> Dict[_K, _V]: ...


def get_in(
        keys: Sequence[Any],
        coll: Mapping[_K, _V],
        default: Any = None,
        no_default: bool = False,
) -> Any: ...


def itemfilter(
        predicate: Callable[[Tuple[_K, _V]], bool],
        d: Mapping[_K, _V],
        factory: Callable[[], Dict[_K, _V]] = dict,
) -> Dict[_K, _V]: ...


def itemmap(
        func: Callable[[Tuple[_K, _V]], Tuple[_K1, _V1]],
        d: Mapping[_K, _V],
        factory: Callable[[], Dict[_K1, _V1]] = dict
) -> Dict[_K1, _V1]: ...


def keyfilter(
        predicate: Callable[[_K], bool],
        d: Mapping[_K, _V],
        factory: Callable[[], Dict[_K, _V]] = dict,
) -> Dict[_K, _V]: ...


def keymap(
        func: Callable[[_K], _K1],
        d: Mapping[_K, _V],
        factory: Callable[[], Dict[_K1, _V]] = dict
) -> Dict[_K1, _V]: ...


def merge(
        *dicts: Mapping[_K, _V],
        factory: Callable[[], Dict[_K, _V]] = dict,
) -> Dict[_K, _V]: ...


@overload
def merge_with(
        func: Callable[[Sequence[_V]], _V1],
        *dicts: Mapping[_K, _V],
        factory: Callable[[], Dict[_K, _V1]] = dict,
) -> Dict[_K, _V1]: ...


@overload
def merge_with(
        func: Callable[[Sequence[Any]], Any],
        *dicts: Mapping[_K, Any],
        factory: Callable[[], Dict[_K, Any]] = dict,
) -> Dict[_K, Any]: ...


def update_in(
        d: Mapping[_K, _V],
        keys: Sequence[Any],
        func: Callable[[Any], Any],
        default: Any = None,
        factory: Callable[[], Dict[_K, Any]] = dict,
) -> Dict[_K, Any]: ...


def valfilter(
        predicate: Callable[[_V], bool],
        d: Mapping[_K, _V],
        factory: Callable[[], Dict[_K, _V]] = dict,
) -> Dict[_K, _V]: ...


def valmap(
        func: Callable[[_V], _V1],
        d: Mapping[_K, _V],
        factory: Callable[[], Dict[_K, _V1]] = dict
) -> Dict[_K, _V1]: ...

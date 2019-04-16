from typing import Any, Callable, TypeVar, overload

_T1 = TypeVar('_T1')
_T2 = TypeVar('_T2')
_T3 = TypeVar('_T3')
_T4 = TypeVar('_T4')
_T5 = TypeVar('_T5')
_T6 = TypeVar('_T6')
_T7 = TypeVar('_T7')
_T8 = TypeVar('_T8')
_T9 = TypeVar('_T9')
_T10 = TypeVar('_T10')
_T11 = TypeVar('_T11')


@overload
def pipe(
        item: _T1,
        func1: Callable[[_T1], _T2],
) -> _T2:
    ...


@overload
def pipe(
        item: _T1,
        func1: Callable[[_T1], _T2],
        func2: Callable[[_T2], _T3],
) -> _T3:
    ...


@overload
def pipe(
        item: _T1,
        func1: Callable[[_T1], _T2],
        func2: Callable[[_T2], _T3],
        func3: Callable[[_T3], _T4],
) -> _T4:
    ...


@overload
def pipe(
        item: _T1,
        func1: Callable[[_T1], _T2],
        func2: Callable[[_T2], _T3],
        func3: Callable[[_T3], _T4],
        func4: Callable[[_T4], _T5],
) -> _T5:
    ...


@overload
def pipe(
        item: _T1,
        func1: Callable[[_T1], _T2],
        func2: Callable[[_T2], _T3],
        func3: Callable[[_T3], _T4],
        func4: Callable[[_T4], _T5],
        func5: Callable[[_T5], _T6],
) -> _T6:
    ...


@overload
def pipe(
        item: _T1,
        func1: Callable[[_T1], _T2],
        func2: Callable[[_T2], _T3],
        func3: Callable[[_T3], _T4],
        func4: Callable[[_T4], _T5],
        func5: Callable[[_T5], _T6],
        func6: Callable[[_T6], _T7],
) -> _T7:
    ...


@overload
def pipe(
        item: _T1,
        func1: Callable[[_T1], _T2],
        func2: Callable[[_T2], _T3],
        func3: Callable[[_T3], _T4],
        func4: Callable[[_T4], _T5],
        func5: Callable[[_T5], _T6],
        func6: Callable[[_T6], _T7],
        func7: Callable[[_T7], _T8],
) -> _T8:
    ...


@overload
def pipe(
        item: _T1,
        func1: Callable[[_T1], _T2],
        func2: Callable[[_T2], _T3],
        func3: Callable[[_T3], _T4],
        func4: Callable[[_T4], _T5],
        func5: Callable[[_T5], _T6],
        func6: Callable[[_T6], _T7],
        func7: Callable[[_T7], _T8],
        func8: Callable[[_T8], _T9],
) -> _T9:
    ...


@overload
def pipe(
        item: _T1,
        func1: Callable[[_T1], _T2],
        func2: Callable[[_T2], _T3],
        func3: Callable[[_T3], _T4],
        func4: Callable[[_T4], _T5],
        func5: Callable[[_T5], _T6],
        func6: Callable[[_T6], _T7],
        func7: Callable[[_T7], _T8],
        func8: Callable[[_T8], _T9],
        func9: Callable[[_T9], _T10],
) -> _T10:
    ...


@overload
def pipe(
        item: _T1,
        func1: Callable[[_T1], _T2],
        func2: Callable[[_T2], _T3],
        func3: Callable[[_T3], _T4],
        func4: Callable[[_T4], _T5],
        func5: Callable[[_T5], _T6],
        func6: Callable[[_T6], _T7],
        func7: Callable[[_T7], _T8],
        func8: Callable[[_T8], _T9],
        func9: Callable[[_T9], _T10],
        func10: Callable[[_T10], _T11],
) -> _T11:
    ...


@overload
def pipe(
        item: Any,
        *funcs: Callable[[Any], Any],
) -> Any:
    ...

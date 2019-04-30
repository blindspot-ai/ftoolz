from typing import Callable, Iterable, overload

from ftoolz.functoolz import A_out


@overload
def generate(
        f: Callable[[int], A_out],
        stop: int
) -> Iterable[A_out]: ...


@overload
def generate(
        f: Callable[[int], A_out],
        start: int,
        stop: int,
        step: int = 1
) -> Iterable[A_out]: ...

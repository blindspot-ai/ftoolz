from typing import Callable, overload

from ftoolz.functoolz import A_out
from ftoolz.typing import Seq


@overload
def generate(
        f: Callable[[int], A_out],
        stop: int
) -> Seq[A_out]: ...


@overload
def generate(
        f: Callable[[int], A_out],
        start: int,
        stop: int,
        step: int = 1
) -> Seq[A_out]: ...

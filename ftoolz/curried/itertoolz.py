from typing import Callable, Iterable, Optional, Tuple

from cytoolz import curry

import ftoolz.itertoolz as it
from ftoolz.typing import Map, Seq

# TODO: Add typing for all levels of curry

PredE = Callable[[it.E], bool]
ItE = Iterable[it.E]
SeqE = Seq[it.E]

associate: Callable[
    [Callable[[it.B], it.A]],
    Callable[[Iterable[it.B]], Map[it.A, it.B]]
] = curry(it.associate)

associate_to: Callable[
    [Callable[[it.B], it.A]],
    Callable[[Callable[[it.B], it.C], Iterable[it.B]], Map[it.A, it.C]]
] = curry(it.associate_to)

find: Callable[[PredE], Callable[[ItE], Optional[it.E]]] = \
    curry(it.find)

split_by: Callable[[PredE], Callable[[ItE], Tuple[ItE, ItE]]] = \
    curry(it.split_by)

take: Callable[[int], Callable[[ItE], SeqE]] = \
    curry(it.take)

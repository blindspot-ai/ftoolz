from typing import List, Tuple, Type
from unittest import TestCase

from ftoolz.unsafe.reflection import implementations


class ReflectionTest(TestCase):

    def test_implementations(self) -> None:
        from tests.test_unsafe.classes import A, B, E

        cases: List[Tuple[Type[A], List[str]]] = [
            (A, ['C', 'D', 'E']),
            (B, ['C', 'D']),
            (E, []),
        ]

        for clz, expected in cases:
            with self.subTest(clz=clz):
                impls = implementations(clz, __package__)
                actual = [c.__name__ for c in impls]
                self.assertListEqual(expected, actual)

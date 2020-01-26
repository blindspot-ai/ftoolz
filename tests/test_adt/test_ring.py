from typing import Any
from unittest import TestCase

from ftoolz.adt.ring import Ring


class RingTest(TestCase):
    maxDiff = None
    _num_shifts = 20

    def test_empty_ring(self) -> None:
        ring: Ring[Any] = Ring()
        self.assertFalse(ring)
        self.assertEqual(0, len(ring))
        self.assertFalse(ring.state())
        self.assertListEqual([], list(ring))

    def test_non_empty_ring(self) -> None:
        ring = Ring(elements=('a', 'b', 'c'))
        num_elements = len(ring)

        self.assertEqual(3, num_elements)

        expected_items = ['a', 'b', 'c']

        for i, actual_item in enumerate(ring):
            if i >= self._num_shifts:
                break
            expected_item = expected_items[i % num_elements]
            self.assertEqual(expected_item, actual_item)

    def test_ring_state(self) -> None:
        ring = Ring(elements=('a', 'b'))
        size = len(ring)

        states = [('a', 'b'), ('b', 'a')]

        for i in range(self._num_shifts):
            self.assertSequenceEqual(states[i % size], ring.state())
            _ = next(ring)

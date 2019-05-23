from abc import ABC, abstractmethod


class A(ABC):
    @abstractmethod
    def test(self) -> None:
        pass

    @abstractmethod
    def test2(self) -> None:
        pass


class B(A, ABC):  # pylint: disable=W0223
    def test(self) -> None:
        pass


class C(B):
    def test2(self) -> None:
        pass


class D(C):
    def test2(self) -> None:
        pass


class E(A):
    def test(self) -> None:
        pass

    def test2(self) -> None:
        pass


class F(E):
    __protected__ = True

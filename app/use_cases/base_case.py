from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

T = TypeVar("T")


class BaseUseCase(ABC, Generic[T]):
    """
    Базовый класс для всех Use Cases.
    Все Use Cases должны наследоваться от этого класса и реализовать метод execute.
    """

    @abstractmethod
    async def execute(self, *args: Any, **kwargs: Any) -> T:
        pass

    @abstractmethod
    async def validate(self, *args: Any, **kwargs: Any):
        pass
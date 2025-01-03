from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar

from sqlalchemy import or_
from sqlalchemy.orm import Query as SQLAlchemyQuery

T = TypeVar("T")


class BasePaginationFilter(Generic[T], ABC):
    def __init__(
        self,
        model: T,
        per_page: int = 20,
        page: int = 1,
        search: Optional[str] = None,
        order_by: Optional[str] = None,
        order_direction: str = "asc",
    ) -> None:
        self.model = model
        self.per_page = per_page
        self.page = page
        self.search = search
        self.order_by = order_by
        self.order_direction = order_direction

    @abstractmethod
    def get_search_filters(self) -> Optional[List[str]]:
        pass

    @abstractmethod
    def apply(self) -> List[SQLAlchemyQuery]:
        pass

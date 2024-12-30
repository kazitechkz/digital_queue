from abc import ABC, abstractmethod
from typing import Any, List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Query as SQLAlchemyQuery


class BasePaginationFilter(ABC):
    def __init__(
        self,
        per_page: int = 20,
        page: int = 1,
        search: Optional[str] = None,
        order_by: Optional[str] = None,
        order_direction: str = "asc",
    ) -> None:
        self.per_page = per_page
        self.page = page
        self.search = search
        self.order_by = order_by
        self.order_direction = order_direction

    @abstractmethod
    def get_search_filters(self) -> Optional[List[str]]:
        pass

    @abstractmethod
    def apply(self, query: SQLAlchemyQuery, model: Any) -> List[SQLAlchemyQuery]:
        pass

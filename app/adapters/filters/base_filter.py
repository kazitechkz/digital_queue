from abc import ABC, abstractmethod
from typing import Any, List, Optional

from sqlalchemy.orm import Query as SQLAlchemyQuery


class BaseFilter(ABC):
    def __init__(
        self,
        search: Optional[str] = None,
        order_by: Optional[str] = None,
        order_direction: Optional[str] = "asc",
    ) -> None:
        self.search = search
        self.order_by = order_by
        self.order_direction = order_direction

    @abstractmethod
    def get_search_filters(self) -> Optional[List[str]]:
        pass

    @abstractmethod
    def apply(self, query: SQLAlchemyQuery, model: Any) -> List[SQLAlchemyQuery]:
        pass

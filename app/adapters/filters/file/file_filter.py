from typing import List, Optional

from fastapi import Depends
from sqlalchemy import and_, inspect, or_
from sqlalchemy.orm import Query as SQLAlchemyQuery

from app.adapters.filters.base_pagination_filter import BasePaginationFilter
from app.entities import FileModel
from app.shared.query_constants import AppQueryConstants


class FileFilter(BasePaginationFilter[FileModel]):
    def __init__(
        self,
        per_page: int = AppQueryConstants.StandardPerPageQuery(),
        page: int = AppQueryConstants.StandardPageQuery(),
        search: Optional[str] = AppQueryConstants.StandardOptionalSearchQuery(
            description="Уникальный поиск по расположению, имени файла, расширению"
        ),
        order_by: Optional[str] = AppQueryConstants.StandardSortFieldQuery(),
        order_direction: Optional[str] = AppQueryConstants.StandardSortDirectionQuery(),
        file_size_more_than_byte: Optional[
            int
        ] = AppQueryConstants.StandardOptionalIntegerQuery(
            description="Укажите размер файла в байтах"
        ),
    ):
        super().__init__(
            model=FileModel,
            search=search,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            per_page=per_page,
        )
        self.file_size_more_than_byte = file_size_more_than_byte

    def get_search_filters(self) -> Optional[List[str]]:
        return [
            "filename",
            "file_path",
            "content_type",
        ]

    def apply(self) -> List[SQLAlchemyQuery]:
        filters = []
        if self.search:
            # Проверяем существование полей в модели
            model_columns = {column.key for column in inspect(self.model).columns}
            search_fields = self.get_search_filters()
            valid_fields = [field for field in search_fields if field in model_columns]
            if valid_fields:
                filters.append(
                    or_(
                        *[
                            getattr(self.model, field).like(f"%{self.search}%")
                            for field in valid_fields
                        ]
                    )
                )
        if self.file_size_more_than_byte:
            filters.append(and_(self.model.file_size >= self.file_size_more_than_byte))
        return filters

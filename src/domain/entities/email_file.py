import time
from typing import List, Optional
from beanie import Document, Link

from src.domain.entities.file_data import FileData


class EmailFile(Document):
    filename: str
    bucket_url: Optional[str] = None
    file_data: Optional[List[FileData]] = []
    created_at: int = int(time.time())
    updated_at: int = int(time.time())

    def get_ordered_users(self, order: str = "asc") -> List[FileData]:
        if order == "asc":
            return sorted(self.file_data, key=lambda x: x.size)
        return sorted(self.file_data, key=lambda x: x.size, reverse=True)
    

    def to_json(self, page: int = 1, order: str = "asc") -> dict:
        limit: int = 100
        list_file_data = []
        self.file_data = sorted(
            self.file_data, key=lambda x: x.size, reverse=True
        )
        self.file_data = self.get_ordered_users(order)
        for file_data in self.file_data[(page - 1) * limit:page * limit]:
            list_file_data.append(file_data.to_json())

        next_page = page + 1 if len(self.file_data) > page * limit else None
        previous_page = page - 1 if len(self.file_data) > (page - 1) * limit else None
        total_pages = len(self.file_data) // limit + 1
        total_data = len(self.file_data)

        return {
            "id": str(self.id),
            "filename": self.filename,
            "bucket_url": self.bucket_url,
            "file_data": list_file_data,
            "created_at": self.created_at,
            "next_page": next_page,
            "previous_page": previous_page,
            "total_pages": total_pages,
            "total_data": total_data
        }
    
    def schema_filename(self) -> str:
        return self.filename


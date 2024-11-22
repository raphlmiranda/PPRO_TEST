from src.domain.entities.base import BaseModel


class FileData(BaseModel):
    username: str
    folder: str
    number_messages: int
    size: int


    def to_json(self) -> dict:
        return {
            "username": self.username,
            "folder": self.folder,
            "numberMessages": self.number_messages,
            "size": self.size
        }

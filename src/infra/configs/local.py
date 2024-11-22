from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    
    MONGO_URI: str
    FOLDER_SAVE_FILES: str
import re
import os
from typing import List
from fastapi import UploadFile

from src.infra.configs.local import Settings
from src.domain.entities.file_data import FileData


class FileUtils:

    def __init__(self, email_file: UploadFile):
        self.email_file = email_file
        self.__settings = Settings()

    @property
    def _get_file_name(self) -> str:
        if not '.' in self.email_file.filename:
            return self.email_file.filename
        return self.email_file.filename.split(".")[0] # caso receba arquivo com extensão

    @property
    def __get_file_extension(self) -> str:
        return self.email_file.filename.split(".")[-1]

    def validate_file_name(self) -> bool:
        regex = re.compile(r'^[A-Za-z0-9-_]+$')
        if re.match(regex, self._get_file_name):
            return True
        return False
    
    def validate_file_extension(self) -> bool:
        allowed_extensions = ['txt']
        if self.__get_file_extension in allowed_extensions:
            return True
        return False
    
    def get_data_from_file(self) -> List[FileData]:
        list_file_data: List[FileData] = []

        with open(f"{self.__settings.FOLDER_SAVE_FILES}{self._get_file_name}", "r") as buffer:
            content = buffer.read()

        lines = content.split('\n')
        for line in lines:
            formated_line = line.split(' ')
            if len(formated_line) > 1:
                list_file_data.append(
                    FileData(
                        username=formated_line[0],
                        folder=formated_line[1],
                        number_messages=formated_line[2],
                        size=formated_line[4]
                    )
                )
        
        return list_file_data
    
    def get_exist_file_in_folder(self) -> bool:
        all_files_in_folder = os.listdir(self.__settings.FOLDER_SAVE_FILES)
        for file in all_files_in_folder:
            if file == self._get_file_name:
                return True
        return False
    
    async def save_file_in_folder(self, file_content: bytes) -> None:
        try:
            file_name = f"{self._get_file_name}"
            
            with open(f"{self.__settings.FOLDER_SAVE_FILES}{file_name}", "wb") as buffer:
                buffer.write(file_content)
                buffer.close()

            return True
    
        except Exception as e:
            return False
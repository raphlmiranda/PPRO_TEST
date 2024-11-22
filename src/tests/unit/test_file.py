import pytest
import os
from fastapi import UploadFile
from unittest.mock import patch, MagicMock

from src.utils.file_utils import FileUtils
from src.infra.configs.local import Settings
from src.domain.entities.file_data import FileData


class MockSettings:
    FOLDER_SAVE_FILES = "/mocked/folder/path/"


class TestFileUtils:

    # @pytest.fixture
    # def mock_folder():
    #     return MockSettings.FOLDER_SAVE_FILES

    # @pytest.fixture
    # def mock_upload_file():
    #     mock_file = UploadFile(filename="test_file.txt", file=MagicMock())
    #     mock_file.file.read.return_value = b"test content"
    #     return mock_file

    # @pytest.fixture
    # def file_utils_instance(mock_upload_file, mock_settings):
    #     with patch.object(FileUtils, "__settings", new_callable=MagicMock, return_value=mock_settings):
    #         return FileUtils(email_file=mock_upload_file)

    @pytest.fixture
    def mock_open(mocker):
        mocked_file = MagicMock()
        mocker.patch("builtins.open", return_value=mocked_file)
        return mocked_file

    def test_get_file_name(self, file_utils_instance):
        assert file_utils_instance._get_file_name == "test_file"

    def test_validate_file_name(self, file_utils_instance):
        assert file_utils_instance.validate_file_name() is True
        

    @patch("builtins.open", new_callable=MagicMock)
    def test_get_data_from_file(self, mock_open, file_utils_instance):
        mock_open.return_value.__enter__.return_value.read.return_value = "user1 folder1 10 size 100\nuser2 folder2 20 size 200"
        
        data = file_utils_instance.get_data_from_file()
        
        expected_data = [
            FileData(username="user1", folder="folder1", number_messages="10", size="100"),
            FileData(username="user2", folder="folder2", number_messages="20", size="200")
        ]
        
        assert data == expected_data

    @patch("os.listdir", return_value=["test_file"])
    def test_get_exist_file_in_folder(self, mock_listdir, file_utils_instance):
        assert file_utils_instance.get_exist_file_in_folder() is True

    @pytest.mark.asyncio
    async def test_save_file_in_folder_success(self, file_utils_instance, mock_upload_file):
        result = await file_utils_instance.save_file_in_folder(mock_upload_file.file.read())
        assert result is True

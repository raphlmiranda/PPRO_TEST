import time
import pytest

from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from fastapi import UploadFile
from unittest.mock import MagicMock

from src.utils.file_utils import FileUtils
from src.domain.entities.email_file import EmailFile
from src.domain.entities.file_data import FileData

@pytest.fixture
def mock_upload_file(mocker):
    mock_file = UploadFile(filename="test_file.txt", file=MagicMock())
    mock_file.file.read.return_value = b"test content"
    return mock_file


@pytest.fixture
def file_utils_instance(mock_upload_file) -> FileUtils:
    return FileUtils(email_file=mock_upload_file)

@pytest.fixture(autouse=True)
async def mongo_mock():
    client = AsyncMongoMockClient()
    await init_beanie(document_models=[EmailFile], database=client.get_database(name="db"))

@pytest.fixture
@pytest.mark.asyncio
async def mock_email_file(mongo_mock):
    mongo_mock = await mongo_mock
    email_mock = await EmailFile(
        filename='valid_input',
        created_at=int(time.time()),
        updated_at=int(time.time()),
        file_data=[
            FileData(
                username='damejoxo@uol.com.br',
                folder='inbox',
                number_messages='002200463',
                size='002142222'
            ),
            FileData(
                username='li_digik@uol.com.br',
                folder='inbox',
                number_messages='011000230',
                size='001032646'
            )
        ],
        bucket_url=None
    ).save()
    return email_mock

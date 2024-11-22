import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient


from src.main import app


client = TestClient(app)

@pytest.fixture
def mock_file_utils():
    with patch('src.utils.file_utils.FileUtils', autospec=True) as mock:
        yield mock

@pytest.mark.asyncio
async def test_create_file_no_file(mock_file_utils, mock_email_file):
    response = client.post(
        "/files",
        files={'email_file': None},
        headers={"Content-Type": 'multipart/form-data;boundary="boundary"'}
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_create_file_invalid_filename():
    multipart_form_data = {
        'email_file': ('invalid input', open('src/tests/unit/invalid input', 'rb')),
    }
    response = client.post(
        "/files",
        files=multipart_form_data,
        headers={"Content-Type": 'multipart/form-data;boundary="boundary"'}
    )
    assert response.status_code == 400
    assert response.content == b"Invalid file name"

@pytest.mark.asyncio
async def test_create_file_new_file(mock_file_utils, mock_email_file):
    mock_file_utils.return_value.validate_file_name.return_value = True
    mock_file_utils.return_value.get_exist_file_in_folder.return_value = False
    mock_email_file = await mock_email_file
    multipart_form_data = {
        'email_file': ('valid_input', open('src/tests/unit/valid_input', 'rb')),
    }
    with patch('src.router.file_router.get_file_content', return_value="damejoxo@uol.com.br inbox 002200463 size 002142222\nli_digik@uol.com.br inbox 011000230 size 001032646"):
        with patch('src.router.file_router.file_background_task'):
            response = client.post(
                "/files",
                files=multipart_form_data,
            )
    assert response.status_code == 201
    assert response.content == b"File uploaded successfully"
    
@pytest.mark.asyncio
async def test_get_content_list_from_filename(mock_email_file):
    mock_email_file = await mock_email_file
    response = client.get(
        f"/files/{mock_email_file.filename}",
        params={'page': 1}
    )
    response_data = response.json()
    
    assert response.status_code == 200
    assert response_data['total_data'] == 2


@pytest.mark.asyncio
async def test_get_asc_order_content_list_from_filename(mock_email_file):
    mock_email_file = await mock_email_file
    response = client.get(
        f"/files/{mock_email_file.filename}",
        params={'page': 1}
    )
    response_data = response.json()
    
    assert response.status_code == 200
    assert response_data['file_data'][0]['username'] == 'li_digik@uol.com.br'

    
@pytest.mark.asyncio
async def test_get_desc_order_content_list_from_filename(mock_email_file):
    mock_email_file = await mock_email_file
    response = client.get(
        f"/files/{mock_email_file.filename}",
        params={'page': 1, 'order': 'desc'}
    )
    response_data = response.json()
    
    assert response.status_code == 200
    assert response_data['file_data'][0]['username'] == 'damejoxo@uol.com.br'

    
@pytest.mark.asyncio
async def test_get_content_list_from_invalid_filename():
    response = client.get(
        "/files/invalid_input",
        params={'page': 1}
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_files(mock_email_file):
    mock_email_file = await mock_email_file
    response = client.get(
        "/files/",
        params={'page': 1}
    )
    response_data = response.json()
    
    assert response.status_code == 200
    assert response_data['total'] == 1
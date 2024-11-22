import time
from typing import List

from fastapi import (
    APIRouter,
    Response,
    UploadFile,
    BackgroundTasks
)

from src.utils.file_utils import FileUtils
from src.domain.entities.email_file import EmailFile


file_router = APIRouter()


async def file_background_task(file_utils: FileUtils, file_content: bytes) -> EmailFile:
    get_file_data = file_utils.get_data_from_file()
    validate_database = await EmailFile.find_one(
        EmailFile.filename == file_utils._get_file_name
    )
    await file_utils.save_file_in_folder(file_content)
    if validate_database:
        validate_database.updated_at = int(time.time())
        validate_database.file_data = get_file_data
        await validate_database.save()
        return validate_database
    
    return await EmailFile(
        filename=file_utils._get_file_name,
        file_data=get_file_data
    ).insert()

async def get_file_content(uploaded_file: UploadFile):
    return await uploaded_file.read()


@file_router.put("/files")
async def create_file(
    email_file: UploadFile,
    background_tasks: BackgroundTasks
) -> Response:
    
    if email_file is None:
        return Response(
            status_code=400,
            content="File is required"
        )
        
    file_utils = FileUtils(email_file)
    if not file_utils.validate_file_name():
        return Response(
            status_code=400,
            content='Invalid file name'
        )
    
    file_content = await get_file_content(email_file)
    
    background_tasks.add_task(file_background_task, file_utils, file_content)

    validate_database = await EmailFile.find_one(
        EmailFile.filename == email_file.filename
    )
    if validate_database is not None:
        if file_utils.get_exist_file_in_folder():
            return Response(
                status_code=204
            )
        
    return Response(
        status_code=201,
        content=f"File uploaded successfully"
    )



@file_router.get("/files/{filename}")
async def get_content_list_from_file(
    filename: str,
    page: int = 1,
    order: str = "asc"
) -> Response:
    
    if page < 1:
        page = 1

    validate_database = await EmailFile.find_one(
        EmailFile.filename == filename
    )
    if validate_database is None:
        return Response(
            status_code=404,
            content="File not found"
        )
    
    return validate_database.to_json(page, order)


@file_router.get("/files/")
async def get_all_files(
    page: int = 1
) -> Response:
    limit = 10
    list_files = []
    if page < 1:
        page = 1

    total_files = await EmailFile.find().count()

    all_files: List[EmailFile] = await EmailFile.find().limit(limit).skip(page - 1).to_list()
    for each_file in all_files:
        list_files.append(each_file.schema_filename())

    next_page = page + 1 if total_files > page * limit else None
    previous_page = page - 1 if page > 1 else None

    return {
        "files": list_files,
        "next_page": next_page,
        "previous_page": previous_page,
        "total": total_files,
    }
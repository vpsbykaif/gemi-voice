from typing import Annotated
from fastapi import APIRouter, Depends, Response
from os import remove

from services.tmp_file_service import TmpFileService

files_api = APIRouter()

@files_api.get("/{uuid}")
async def files(uuid: str, fileSvc: Annotated[TmpFileService, Depends(TmpFileService)]):
    path = fileSvc.get_path(uuid)
    if not path:
        return Response(content="Not found", status_code=404)
    
    with open(path, "rb") as file:
        return Response(content=file.read(), media_type="audio/x-wav")

@files_api.get("/onetime/{uuid}")
async def files(uuid: str, fileSvc: Annotated[TmpFileService, Depends(TmpFileService)]):
    path = fileSvc.remove_path(uuid)
    if not path:
        return Response(content="Not found", status_code=404)
    
    file_bin: bytes = None
    with open(path, "rb") as file:
        file_bin = file.read()
    remove(path)
    return Response(content=file_bin, media_type="audio/x-wav")
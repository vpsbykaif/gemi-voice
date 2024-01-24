from typing import Annotated
from fastapi import Depends, APIRouter, UploadFile
from pydantic import BaseModel

from stt.vosk import VoskRecognizer

listen_api = APIRouter()

@listen_api.post("/vosk")
async def listen(file: UploadFile, vosk: Annotated[VoskRecognizer, Depends(VoskRecognizer)]):
    file_type = file.content_type
    return { "text": await vosk.listen(file) }

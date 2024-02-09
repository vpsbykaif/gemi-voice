from typing import Annotated
from fastapi import Depends, APIRouter, UploadFile
from pydantic import BaseModel

from stt.vosk import VoskRecognizer
from stt.wit import WitRecognizer

listen_api = APIRouter()

@listen_api.post("/vosk")
async def listen(file: UploadFile, vosk: Annotated[VoskRecognizer, Depends(VoskRecognizer)]):
    return { "text": await vosk.listen(file) }

@listen_api.post("/wit")
async def listen(file: UploadFile, vosk: Annotated[WitRecognizer, Depends(WitRecognizer)]):
    return { "text": await vosk.listen(file) }

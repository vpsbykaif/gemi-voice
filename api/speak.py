from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response
from services.tmp_file_service import TmpFileService
from tts.festival import FestivalTTS
from tts.flite import FliteTTS
from pydantic import BaseModel

speak_api = APIRouter()

class Speak(BaseModel):
    voice_id: str
    text: str

def flite_init():
    return FliteTTS('voices/flite')

@speak_api.get("/festival")
async def festival(text: str, voice_id: str, tts: Annotated[FestivalTTS, Depends(FestivalTTS)]):
    async for voice in tts.voices():
        if voice.id == voice_id:
            return Response(content=await tts.say(text, voice_id), media_type="audio/x-wav")
    return Response(content="Voice not found", status_code=400)

@speak_api.post("/festival")
async def festival(speak: Speak, req: Request, tts: Annotated[FestivalTTS, Depends(FestivalTTS)], fileSvc: Annotated[TmpFileService, Depends(TmpFileService)]):
    async for voice in tts.voices():
        if voice.id == speak.voice_id:
            file_name = await tts.save(speak.text, speak.voice_id)
            file_uuid = fileSvc.add_path(file_name)
            return { "url": f"{req.base_url.scheme}://{req.base_url.hostname}/api/files/onetime/{file_uuid}", "type": "audio/x-wav" }
    return Response(content="Voice not found", status_code=400)

@speak_api.get("/flite")
async def flite(text: str, voice_id: str, tts: Annotated[FliteTTS, Depends(flite_init)]):
    async for voice in tts.voices():
        if voice.id == voice_id:
            return Response(content=await tts.say(text, voice_id), media_type="audio/x-wav")
    return Response(content="Voice not found", status_code=400)

@speak_api.post("/flite")
async def flite(speak: Speak, req: Request, tts: Annotated[FliteTTS, Depends(flite_init)], fileSvc: Annotated[TmpFileService, Depends(TmpFileService)]):
    async for voice in tts.voices():
        if voice.id == speak.voice_id:
            file_name = await tts.save(speak.text, speak.voice_id)
            file_uuid = fileSvc.add_path(file_name)
            return { "url": f"{req.base_url.scheme}://{req.base_url.hostname}/api/files/onetime/{file_uuid}", "type": "audio/x-wav" }
    return Response(content="Voice not found", status_code=400)

@speak_api.get("/voices")
async def voices(gender: str | None = None, festival: Annotated[FestivalTTS, Depends(FestivalTTS)] = None, flite: Annotated[FliteTTS, Depends(flite_init)] = None):
    voices = {
        "festival": [voice.id async for voice in festival.voices() if gender is None or voice.gender == gender.capitalize()],
        "flite": [voice.id async for voice in flite.voices() if gender is None or voice.gender == gender.capitalize()],
    }

    return voices
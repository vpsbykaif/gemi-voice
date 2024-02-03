from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response
from services.tmp_file_service import TmpFileService
from tts.base import Voice
from tts.edge import EdgeTTS
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

@speak_api.get("/edge")
async def edge(text: str, voice_id: str, tts: Annotated[EdgeTTS, Depends(EdgeTTS)]):
    async for voice in tts.voices():
        if voice.id == voice_id:
            return Response(content=await tts.say(text, voice_id), media_type="audio/mpeg")
    return Response(content="Voice not found", status_code=400)

@speak_api.post("/edge")
async def edge(speak: Speak, req: Request, tts: Annotated[EdgeTTS, Depends(EdgeTTS)], fileSvc: Annotated[TmpFileService, Depends(TmpFileService)]):
    async for voice in tts.voices():
        if voice.id == speak.voice_id:
            file_name = await tts.save(speak.text, speak.voice_id)
            file_uuid = fileSvc.add_path(file_name)
            return { "url": f"{req.base_url.scheme}://{req.base_url.hostname}/api/files/onetime/{file_uuid}", "type": "audio/mpeg" }
    return Response(content="Voice not found", status_code=400)

@speak_api.get("/voices")
async def voices(
        language: str | None = None,
        gender: str | None = None,
        festival: Annotated[FestivalTTS, Depends(FestivalTTS)] = None,
        flite: Annotated[FliteTTS, Depends(flite_init)] = None,
        edge: Annotated[EdgeTTS, Depends(EdgeTTS)] = None
    ):
    def filter_voice(voice: Voice):
        return (gender is None or voice.gender == gender.capitalize()) and (language is None or voice.language == language.lower())

    voices = {
        "festival": [voice.id async for voice in festival.voices() if filter_voice(voice)],
        "flite": [voice.id async for voice in flite.voices() if filter_voice(voice)],
        "edge": [voice.id async for voice in edge.voices() if filter_voice(voice)],
    }

    return voices
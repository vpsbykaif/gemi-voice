import asyncio
import json
import tempfile
from fastapi import UploadFile
from speech_recognition import Recognizer, AudioFile
from vosk import Model
from os import listdir

class VoskRecognizer:
    rec: Recognizer

    def __init__(self):
        self.rec = Recognizer()
        model = [model for model in listdir("models") if model.startswith("vosk-model")][0]
        self.rec.vosk_model = Model(f"models/{model}")

    async def convert_to_wav(self, audio_bytes: bytes, wav_path: str):
        command = ['ffmpeg', '-i', '-', '-acodec', 'pcm_s16le',
               '-ar', '11025', '-ac', '1', '-y', wav_path]
        proc = await asyncio.create_subprocess_exec(
            *command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE
        )
        await proc.communicate(input=audio_bytes)

    async def listen(self, upload_file: UploadFile) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav") as wav_file:
            await self.convert_to_wav(upload_file.file.read(), wav_file.name)
            wav_file.seek(0)
            with AudioFile(wav_file) as audio_file:
                audio_data = self.rec.record(audio_file)
                return json.loads(self.rec.recognize_vosk(audio_data))['text']
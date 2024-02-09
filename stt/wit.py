import asyncio
import tempfile
from fastapi import UploadFile
from speech_recognition import Recognizer, AudioFile
from os import getenv

class WitRecognizer:
    api_key: str
    rec: Recognizer

    def __init__(self):
        self.api_key = getenv("WIT_AI_API_KEY")
        self.rec = Recognizer()

    async def convert_to_wav(self, audio_bytes: bytes, wav_path: str):
        command = ['ffmpeg', '-i', '-', '-y', wav_path]
        proc = await asyncio.create_subprocess_exec(
            *command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE
        )
        await proc.communicate(input=audio_bytes)

    async def listen(self, upload_file: UploadFile) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav") as wav_file:
            if ['audio/wav', 'audio/x-wav', 'audio/wave', 'audio/x-pn-wav'].__contains__(upload_file.content_type):
                wav_file.write(upload_file.file.read())
            else:
                await self.convert_to_wav(upload_file.file.read(), wav_file.name)
            wav_file.seek(0)
            with AudioFile(wav_file) as audio_file:
                audio_data = self.rec.record(audio_file)
                return self.rec.recognize_wit(audio_data, key=self.api_key)
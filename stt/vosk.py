import json
from fastapi import UploadFile
from speech_recognition import Recognizer, AudioFile
from vosk import Model

class VoskRecognizer:
    rec: Recognizer

    def __init__(self):
        self.rec = Recognizer()
        self.rec.vosk_model = Model("models/vosk-model-en-in-0.5")

    async def listen(self, upload_file: UploadFile) -> str:
        with AudioFile(upload_file.file) as audio_file:
            audio_data = self.rec.record(audio_file)
            return json.loads(self.rec.recognize_vosk(audio_data))['text']
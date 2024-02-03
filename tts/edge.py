import logging
import tempfile
from edge_tts import list_voices, Communicate

from tts.base import TTSBase, Voice, VoicesIterable

_LOGGER = logging.getLogger(__name__)

class EdgeTTS(TTSBase):
    async def voices(self) -> VoicesIterable:
        for voice in await list_voices():
            yield Voice(
                id=voice["ShortName"],
                name=voice["FriendlyName"],
                gender=str(voice["Gender"])[0],
                locale=voice["Locale"],
                language=str(voice["Locale"]).split("-")[0],
            )

    async def _voice_by_id(self, voice_id: str) -> Voice:
        for voice in await list_voices():
            if voice["ShortName"] == voice_id:
                return Voice(
                    id=voice["ShortName"],
                    name=voice["FriendlyName"],
                    gender=str(voice["Gender"])[0],
                    locale=voice["Locale"],
                    language=str(voice["Locale"]).split("-")[0],
                )

    async def say(self, text: str, voice_id: str, **kwargs) -> bytes:
        """Speak text as MP3."""

        # Look up voices by voice_id
        voice = await self._voice_by_id(voice_id)

        with tempfile.NamedTemporaryFile(suffix=".mp3") as mp3_file:
            communicate = Communicate(text=text, voice=voice.id)

            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    mp3_file.write(chunk["data"])

            mp3_file.seek(0)
            return mp3_file.read()

    async def save(self, text: str, voice_id: str, **kwargs) -> str:
        """Speak text as MP3."""

        # Look up voices by voice_id
        voice = await self._voice_by_id(voice_id)

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as mp3_file:
            communicate = Communicate(text=text, voice=voice.id)

            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    mp3_file.write(chunk["data"])

            return mp3_file.name
from abc import ABCMeta
from dataclasses import dataclass
import typing


@dataclass
class Voice:
    """Single TTS voice."""

    id: str
    name: str
    gender: str
    language: str
    locale: str
    tag: typing.Optional[typing.Dict[str, typing.Any]] = None
    multispeaker: bool = False
    speakers: typing.Optional[typing.Dict[str, int]] = None


VoicesIterable = typing.AsyncGenerator[Voice, None]


class TTSBase(metaclass=ABCMeta):
    """Base class of TTS systems."""

    async def voices(self) -> VoicesIterable:
        """Get list of available voices."""
        yield Voice("", "", "", "", "")

    async def say(self, text: str, voice_id: str, **kwargs) -> bytes:
        """Speak text as WAV."""
        return bytes()
    
    async def save(self, text: str, voice_id: str, **kwargs) -> str:
        """Save text as WAV."""
        return str()
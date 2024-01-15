import asyncio
import logging
import shlex
import typing
from pathlib import Path

from tts.base import TTSBase, Voice, VoicesIterable

_LOGGER = logging.getLogger(__name__)

class FliteTTS(TTSBase):
    """Wraps flite (http://www.festvox.org/flite)"""

    def __init__(self, voice_dir: typing.Union[str, Path]):
        self.voice_dir = Path(voice_dir)

    async def voices(self) -> VoicesIterable:
        """Get list of available voices."""
        flite_voices = [
            # English
            Voice(
                id="cmu_us_aew",
                name="cmu_us_aew",
                gender="M",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_ahw",
                name="cmu_us_ahw",
                gender="M",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_aup",
                name="cmu_us_aup",
                gender="M",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_awb",
                name="cmu_us_awb",
                gender="M",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_axb",
                name="cmu_us_axb",
                gender="F",
                locale="en-in",
                language="en",
            ),
            Voice(
                id="cmu_us_bdl",
                name="cmu_us_bdl",
                gender="M",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_clb",
                name="cmu_us_clb",
                gender="F",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_eey",
                name="cmu_us_eey",
                gender="F",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_fem",
                name="cmu_us_fem",
                gender="M",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_gka",
                name="cmu_us_gka",
                gender="M",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_jmk",
                name="cmu_us_jmk",
                gender="M",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_ksp",
                name="cmu_us_ksp",
                gender="M",
                locale="en-in",
                language="en",
            ),
            Voice(
                id="cmu_us_ljm",
                name="cmu_us_ljm",
                gender="F",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_lnh",
                name="cmu_us_lnh",
                gender="F",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_rms",
                name="cmu_us_rms",
                gender="M",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_rxr",
                name="cmu_us_rxr",
                gender="M",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="cmu_us_slp",
                name="cmu_us_slp",
                gender="F",
                locale="en-in",
                language="en",
            ),
            Voice(
                id="cmu_us_slt",
                name="cmu_us_slt",
                gender="F",
                locale="en-us",
                language="en",
            ),
            Voice(
                id="mycroft_voice_4.0",
                name="mycroft_voice_4.0",
                gender="M",
                locale="en-us",
                language="en",
            ),
            # Indic
            Voice(
                id="cmu_indic_hin_ab",
                name="cmu_indic_hin_ab",
                gender="F",
                locale="hi-in",
                language="hi",
            ),
            Voice(
                id="cmu_indic_ben_rm",
                name="cmu_indic_ben_rm",
                gender="F",
                locale="bn-in",
                language="bn",
            ),
            Voice(
                id="cmu_indic_guj_ad",
                name="cmu_indic_guj_ad",
                gender="F",
                locale="gu-in",
                language="gu",
            ),
            Voice(
                id="cmu_indic_guj_dp",
                name="cmu_indic_guj_dp",
                gender="F",
                locale="gu-in",
                language="gu",
            ),
            Voice(
                id="cmu_indic_guj_kt",
                name="cmu_indic_guj_kt",
                gender="F",
                locale="gu-in",
                language="gu",
            ),
            Voice(
                id="cmu_indic_kan_plv",
                name="cmu_indic_kan_plv",
                gender="F",
                locale="kn-in",
                language="kn",
            ),
            Voice(
                id="cmu_indic_mar_aup",
                name="cmu_indic_mar_aup",
                gender="F",
                locale="mr-in",
                language="mr",
            ),
            Voice(
                id="cmu_indic_mar_slp",
                name="cmu_indic_mar_slp",
                gender="F",
                locale="mr-in",
                language="mr",
            ),
            Voice(
                id="cmu_indic_pan_amp",
                name="cmu_indic_pan_amp",
                gender="F",
                locale="pa-in",
                language="pa",
            ),
            Voice(
                id="cmu_indic_tam_sdr",
                name="cmu_indic_tam_sdr",
                gender="F",
                locale="ta-in",
                language="ta",
            ),
            Voice(
                id="cmu_indic_tel_kpn",
                name="cmu_indic_tel_kpn",
                gender="F",
                locale="te-in",
                language="te",
            ),
            Voice(
                id="cmu_indic_tel_sk",
                name="cmu_indic_tel_sk",
                gender="F",
                locale="te-in",
                language="te",
            ),
            Voice(
                id="cmu_indic_tel_ss",
                name="cmu_indic_tel_ss",
                gender="F",
                locale="te-in",
                language="te",
            ),
        ]

        for voice in flite_voices:
            voice_path = self.voice_dir / f"{voice.id}.flitevox"
            if voice_path.is_file():
                yield voice

    async def say(self, text: str, voice_id: str, **kwargs) -> bytes:
        """Speak text as WAV."""
        flite_cmd = [
            "flite",
            "-voice",
            shlex.quote(str(self.voice_dir / f"{voice_id}.flitevox")),
            "-o",
            "/dev/stdout",
            "-t",
            shlex.quote(text),
        ]
        _LOGGER.debug(flite_cmd)

        proc = await asyncio.create_subprocess_exec(
            *flite_cmd, stdout=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        return stdout

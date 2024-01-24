import asyncio
import logging
import shutil
import tempfile
import typing
from tts.base import TTSBase, Voice, VoicesIterable

_LOGGER = logging.getLogger(__name__)

class FestivalTTS(TTSBase):
    """Wraps festival (http://www.cstr.ed.ac.uk/projects/festival/)"""

    # Single byte text encodings for specific languages.
    # See https://en.wikipedia.org/wiki/ISO/IEC_8859
    #
    # Some encodings differ from linked article (part 1 is missing relevant
    # symbols).
    LANGUAGE_ENCODINGS = {
        "en": "iso-8859-1",
        "ru": "iso-8859-1",  # Russian is transliterated below
        "es": "iso-8859-15",  # Differs from linked article
        "ca": "iso-8859-15",  # Differs from linked article
        "cs": "iso-8859-2",
        "fi": "iso-8859-15",  # Differs from linked article
        "ar": "utf-8",
    }

    FESTIVAL_VOICES = [
        # English
        Voice(
            id="us1_mbrola",
            name="us1_mbrola",
            gender="F",
            locale="en-us",
            language="en",
        ),
        Voice(
            id="us2_mbrola",
            name="us2_mbrola",
            gender="M",
            locale="en-us",
            language="en",
        ),
        Voice(
            id="us3_mbrola",
            name="us3_mbrola",
            gender="M",
            locale="en-us",
            language="en",
        ),
        Voice(
            id="rab_diphone",
            name="rab_diphone",
            gender="M",
            locale="en-gb",
            language="en",
        ),
        Voice(
            id="en1_mbrola",
            name="en1_mbrola",
            gender="M",
            locale="en-us",
            language="en",
        ),
        Voice(
            id="ked_diphone",
            name="ked_diphone",
            gender="M",
            locale="en-us",
            language="en",
        ),
        Voice(
            id="kal_diphone",
            name="kal_diphone",
            gender="M",
            locale="en-us",
            language="en",
        ),
        Voice(
            id="cmu_us_slt_arctic_hts",
            name="cmu_us_slt_arctic_hts",
            gender="F",
            locale="en-us",
            language="en",
        ),
        # Russian
        Voice(
            id="msu_ru_nsh_clunits",
            name="msu_ru_nsh_clunits",
            gender="M",
            locale="ru-ru",
            language="ru",
        ),
        # Spanish
        Voice(
            id="el_diphone",
            name="el_diphone",
            gender="M",
            locale="es-es",
            language="es",
        ),
        # Catalan
        Voice(
            id="upc_ca_ona_hts",
            name="upc_ca_ona_hts",
            gender="F",
            locale="ca-es",
            language="ca",
        ),
        # Czech
        Voice(
            id="czech_dita",
            name="czech_dita",
            gender="F",
            locale="cs-cz",
            language="cs",
        ),
        Voice(
            id="czech_machac",
            name="czech_machac",
            gender="M",
            locale="cs-cz",
            language="cs",
        ),
        Voice(
            id="czech_ph", name="czech_ph", gender="M", locale="cs-cz", language="cs"
        ),
        Voice(
            id="czech_krb", name="czech_krb", gender="F", locale="cs-cz", language="cs"
        ),
        # Finnish
        Voice(
            id="suo_fi_lj_diphone",
            name="suo_fi_lj_diphone",
            gender="F",
            locale="fi-fi",
            language="fi",
        ),
        Voice(
            id="hy_fi_mv_diphone",
            name="hy_fi_mv_diphone",
            gender="M",
            locale="fi-fi",
            language="fi",
        ),
        # Telugu
        Voice(
            id="telugu_NSK_diphone",
            name="telugu_NSK_diphone",
            gender="M",
            locale="te-in",
            language="te",
        ),
        # Marathi
        Voice(
            id="marathi_NSK_diphone",
            name="marathi_NSK_diphone",
            gender="M",
            locale="mr-in",
            language="mr",
        ),
        # Hindi
        Voice(
            id="hindi_NSK_diphone",
            name="hindi_NSK_diphone",
            gender="M",
            locale="hi-in",
            language="hi",
        ),
        # Italian
        Voice(
            id="lp_diphone",
            name="lp_diphone",
            gender="F",
            locale="it-it",
            language="it",
        ),
        Voice(
            id="pc_diphone",
            name="pc_diphone",
            gender="M",
            locale="it-it",
            language="it",
        ),
        # Arabic
        Voice(
            id="ara_norm_ziad_hts",
            name="ara_norm_ziad_hts",
            gender="M",
            locale="ar",
            language="ar",
        ),
    ]

    def __init__(self):
        self._voice_by_id = {v.id: v for v in FestivalTTS.FESTIVAL_VOICES}

    async def voices(self) -> VoicesIterable:
        """Get list of available voices."""
        available_voices: typing.Set[str] = set()

        if shutil.which("festival"):
            try:
                proc = await asyncio.create_subprocess_exec(
                    "festival",
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                )

                list_command = "(print (voice.list))"
                proc_stdout, _ = await proc.communicate(input=list_command.encode())
                list_result = proc_stdout.decode()

                # (voice1 voice2 ...)
                available_voices = set(list_result[1:-2].split())
                _LOGGER.debug("Festival voices: %s", available_voices)
            except Exception:
                _LOGGER.exception("Failed to get festival voices")

        for voice in FestivalTTS.FESTIVAL_VOICES:
            if (not available_voices) or (voice.id in available_voices):
                yield voice

    async def say(self, text: str, voice_id: str, **kwargs) -> bytes:
        """Speak text as WAV."""
        # Default to part 15 encoding to handle "special" characters.
        # See https://www.web3.lu/character-encoding-for-festival-tts-files/
        encoding = "iso-8859-15"

        # Look up encoding by language
        voice = self._voice_by_id.get(voice_id)
        if voice:
            encoding = FestivalTTS.LANGUAGE_ENCODINGS.get(voice.language, encoding)

        with tempfile.NamedTemporaryFile(suffix=".wav") as wav_file:
            festival_cmd = [
                "text2wave",
                "-o",
                wav_file.name,
                "-eval",
                f"(voice_{voice_id})",
            ]
            _LOGGER.debug(festival_cmd)

            proc = await asyncio.create_subprocess_exec(
                *festival_cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
            )
            await proc.communicate(input=text.encode(encoding=encoding))

            wav_file.seek(0)
            return wav_file.read()
        
    async def save(self, text: str, voice_id: str, **kwargs):
        """Speak text as WAV."""
        # Default to part 15 encoding to handle "special" characters.
        # See https://www.web3.lu/character-encoding-for-festival-tts-files/
        encoding = "iso-8859-15"

        # Look up encoding by language
        voice = self._voice_by_id.get(voice_id)
        if voice:
            encoding = FestivalTTS.LANGUAGE_ENCODINGS.get(voice.language, encoding)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as wav_file:
            festival_cmd = [
                "text2wave",
                "-o",
                wav_file.name,
                "-eval",
                f"(voice_{voice_id})",
            ]
            _LOGGER.debug(festival_cmd)

            proc = await asyncio.create_subprocess_exec(
                *festival_cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
            )
            await proc.communicate(input=text.encode(encoding=encoding))

            return wav_file.name

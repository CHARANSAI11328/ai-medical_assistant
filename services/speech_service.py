import base64
import io
import re
import logging
from typing import Optional
from functools import lru_cache

logger = logging.getLogger(__name__)

class SpeechService:
    """
    Multilingual Text-to-Speech service using gTTS.
    Converts text to MP3 audio bytes for seamless, glitch-free playback in Streamlit.
    """

    @staticmethod
    def sanitize_text_for_speech(text: str) -> str:
        """
        Strips markdown syntax, HTML tags, emojis, and formatting artifacts.
        Produces clean, natural spoken clinical speech without reading aloud
        symbols like asterisks, brackets, or code tokens.
        """
        if not text:
            return ""

        # 1. Remove HTML tags
        clean = re.sub(r'<[^>]+>', ' ', text)

        # 2. Remove markdown links [text](url) -> text
        clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean)

        # 3. Remove bold, italic, code formatting
        clean = re.sub(r'[*_~`#>]', ' ', clean)

        # 4. Remove bullet point markers like - or • or numbers at line starts
        clean = re.sub(r'^\s*[-•*]\s+', '', clean, flags=re.MULTILINE)
        clean = re.sub(r'^\s*\d+\.\s+', '', clean, flags=re.MULTILINE)

        # 5. Remove common emoji ranges so TTS doesn't read out emoji descriptions
        clean = re.sub(r'[\U00010000-\U0010ffff]', '', clean)
        clean = re.sub(r'[\u2600-\u27BF]', '', clean)

        # 6. Normalize whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()

        # 7. Extract the first 2-3 complete sentences (up to ~350 chars)
        # Avoid cutting words in half which causes audio glitching/stuttering
        sentences = re.split(r'(?<=[.!?])\s+', clean)
        spoken_summary = []
        total_len = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            spoken_summary.append(sentence)
            total_len += len(sentence)
            if total_len >= 300 or len(spoken_summary) >= 3:
                break

        result = " ".join(spoken_summary).strip()
        return result if result else clean[:300].strip()

    @staticmethod
    def text_to_speech(text: str, lang: str = "en") -> Optional[bytes]:
        """
        Converts text to speech audio bytes (MP3 format).
        Sanitizes text and synthesizes clean natural voice.
        Returns None if gTTS is unavailable or fails.
        """
        clean_text = SpeechService.sanitize_text_for_speech(text)
        if not clean_text or len(clean_text) == 0:
            return None

        # Map language codes
        tts_lang = "en"
        tld = "com"
        if lang in ["hi", "hindi"]:
            tts_lang = "hi"
            tld = "co.in"
        elif lang in ["te", "telugu"]:
            tts_lang = "te"
            tld = "co.in"

        try:
            from gtts import gTTS
            tts = gTTS(text=clean_text, lang=tts_lang, tld=tld, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            audio_bytes = fp.getvalue()
            return audio_bytes if len(audio_bytes) > 0 else None
        except Exception as e:
            logger.warning(f"gTTS Speech synthesis error: {e}")
            return None

    @staticmethod
    def get_audio_html(audio_bytes: bytes) -> str:
        """Generates HTML5 audio player tag with embedded base64 audio."""
        b64 = base64.b64encode(audio_bytes).decode("utf-8")
        return f'<audio controls style="width: 100%; margin-top: 8px;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

import base64
import io
import logging
from typing import Optional

class SpeechService:
    """
    Multilingual Text-to-Speech service using gTTS.
    Converts text to MP3 audio bytes for playback in Streamlit.
    """
    @staticmethod
    def text_to_speech(text: str, lang: str = "en") -> Optional[bytes]:
        """
        Converts text to speech audio bytes (MP3 format).
        Returns None if gTTS is unavailable or fails.
        """
        if not text or len(text.strip()) == 0:
            return None

        # Truncate extremely long text for audio efficiency
        clean_text = text[:500]
        
        # Map lang codes
        tts_lang = "en"
        if lang in ["hi", "hindi"]:
            tts_lang = "hi"
        elif lang in ["te", "telugu"]:
            tts_lang = "te"

        try:
            from gtts import gTTS
            tts = gTTS(text=clean_text, lang=tts_lang, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.getvalue()
        except Exception as e:
            logging.warning(f"gTTS Speech synthesis error: {e}")
            return None

    @staticmethod
    def get_audio_html(audio_bytes: bytes) -> str:
        """Generates HTML5 audio player tag with embedded base64 audio."""
        b64 = base64.b64encode(audio_bytes).decode("utf-8")
        return f'<audio controls autoplay style="width: 100%; margin-top: 10px;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

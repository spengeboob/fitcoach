"""MiMo TTS voice generation for FitCoach."""

import logging
import tempfile
import httpx

logger = logging.getLogger("fitcoach.voice")


class VoiceDelivery:
    """Generate voice briefings using MiMo TTS."""

    def __init__(self, mimo_api_key: str):
        self.api_key = mimo_api_key

    async def generate(self, text: str) -> str | None:
        """Generate voice audio from text. Returns file path or None."""
        if not self.api_key:
            logger.warning("MiMo API key not set — skipping voice")
            return None

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.xiaomimimo.com/v1/audio/speech",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "mimo-tts",
                        "input": text[:4096],
                        "voice": "alloy",
                    },
                    timeout=60,
                )

                if resp.status_code == 200:
                    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
                        f.write(resp.content)
                        return f.name
                else:
                    logger.error("TTS failed: %s", resp.text)
                    return None

        except Exception as e:
            logger.error("Voice generation error: %s", e)
            return None

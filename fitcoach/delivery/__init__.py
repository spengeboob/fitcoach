"""Telegram delivery for FitCoach."""

import logging
import httpx

logger = logging.getLogger("fitcoach.telegram")


class TelegramDelivery:
    """Send and receive messages via Telegram Bot API."""

    BASE_URL = "https://api.telegram.org/bot{token}"

    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.base_url = self.BASE_URL.format(token=token)

    async def get_updates(self, offset: int = 0) -> list[dict]:
        """Get new messages."""
        if not self.token:
            return []

        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base_url}/getUpdates",
                params={"offset": offset, "timeout": 1},
                timeout=5,
            )
            if resp.status_code == 200:
                return resp.json().get("result", [])
            return []

    async def send(self, text: str):
        """Send a text message."""
        if not self.token or not self.chat_id:
            logger.warning("Telegram not configured")
            return

        async with httpx.AsyncClient() as client:
            await client.post(
                f"{self.base_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": "HTML",
                },
                timeout=10,
            )

    async def send_voice(self, file_path: str):
        """Send a voice message."""
        if not self.token or not self.chat_id:
            return

        async with httpx.AsyncClient() as client:
            with open(file_path, "rb") as f:
                await client.post(
                    f"{self.base_url}/sendVoice",
                    data={"chat_id": self.chat_id},
                    files={"voice": f},
                    timeout=30,
                )

    async def download_file(self, file_id: str) -> str | None:
        """Download a file from Telegram."""
        import tempfile

        async with httpx.AsyncClient() as client:
            # Get file path
            resp = await client.get(
                f"{self.base_url}/getFile",
                params={"file_id": file_id},
                timeout=10,
            )
            if resp.status_code != 200:
                return None

            file_path = resp.json()["result"]["file_path"]

            # Download file
            url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
            resp = await client.get(url, timeout=30)

            if resp.status_code == 200:
                suffix = file_path.split(".")[-1] if "." in file_path else ".jpg"
                with tempfile.NamedTemporaryFile(suffix=f".{suffix}", delete=False) as f:
                    f.write(resp.content)
                    return f.name

            return None

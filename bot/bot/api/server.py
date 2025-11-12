import os
from typing import Any, Dict

from fastapi import FastAPI, HTTPException, Request, status

from bot.core.bot_client import bot
from bot.core.logger import logger

app = FastAPI()
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))


async def _resolve_channel():
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        channel = await bot.fetch_channel(CHANNEL_ID)
    return channel


@app.post("/send")
async def send_message(request: Request) -> Dict[str, Any]:
    if CHANNEL_ID <= 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="DISCORD_CHANNEL_ID is not configured",
        )

    data = await request.json()
    msg = data.get("message", "Hello from API!")

    if not bot.is_ready():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Bot not ready")

    try:
        channel = await _resolve_channel()
        await channel.send(msg)
        logger.info(f"📨 Message sent: {msg}")
    except Exception as exc:  # pragma: no cover - defensive logging
        logger.exception("⚠️ Send error")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    return {"status": "ok", "message": msg}

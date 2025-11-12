from fastapi import FastAPI, Request
import asyncio
from bot.core.bot_client import bot
from bot.core.logger import logger
import os

app = FastAPI()
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID", "0"))


@app.post("/send")
async def send_message(request: Request):
    data = await request.json()
    msg = data.get("message", "Hello from API!")

    async def _send():
        try:
            channel = bot.get_channel(CHANNEL_ID)
            if channel is None:
                channel = await bot.fetch_channel(CHANNEL_ID)
            await channel.send(msg)
            logger.info(f"📨 Message sent: {msg}")
        except Exception as e:
            logger.error(f"⚠️ Send error: {e}")

    # Проверяем, что бот действительно запущен и loop активен
    if not bot.is_ready():
        return {"status": "error", "detail": "Bot not ready"}

    try:
        future = asyncio.run_coroutine_threadsafe(_send(), bot.loop)
        # Ждём результат (опционально — можно убрать .result() если не нужен блокирующий вызов)
        future.result()
        return {"status": "ok", "message": msg}
    except Exception as e:
        logger.error(f"⚠️ Exception submitting coroutine: {e}")
        return {"status": "error", "detail": str(e)}

import threading
import asyncio
import uvicorn
from bot.core.bot_client import bot, TOKEN, load_modules
from bot.api.server import app
from bot.core.logger import logger


def start_api():
    uvicorn.run(app, host="0.0.0.0", port=8081, log_level="info")


async def start_bot():
    await load_modules()
    await bot.start(TOKEN)

if __name__ == "__main__":
    threading.Thread(target=start_api, daemon=True).start()

    # Discord бот в главном потоке
    asyncio.run(start_bot())

import asyncio
import contextlib
import uvicorn
from bot.core.bot_client import bot, TOKEN, load_modules
from bot.api.server import app
from bot.core.logger import logger


async def start_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=8081, log_level="info", loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await load_modules()
    api_task = asyncio.create_task(start_api())

    try:
        await bot.start(TOKEN)
    finally:
        if not api_task.done():
            api_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await api_task


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Shutdown requested")

import logging
from logging.handlers import RotatingFileHandler
import os

os.makedirs("logs", exist_ok=True)

file_handler = RotatingFileHandler(
    filename="logs/bot.log",
    mode="a",
    maxBytes=10 * 1024 * 1024,
    backupCount=2,
    encoding="utf-8",
    delay=False
)

stream_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[file_handler, stream_handler]
)

logger = logging.getLogger("discord-bot")
discord_logger = logging.getLogger("discord")
discord_logger.setLevel(logging.WARNING)

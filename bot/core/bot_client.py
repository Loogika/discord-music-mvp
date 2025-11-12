import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

from .logger import logger

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("BOT_PREFIX", "!")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.event
async def on_ready():
    logger.info(f"🤖 Logged in as {bot.user} (ID: {bot.user.id})")


async def load_modules():
    modules_path = Path(__file__).parent.parent / "modules"

    if not modules_path.exists():
        logger.info(f"ℹ️ Modules directory not found at {modules_path}, skipping extension loading")
        return

    for filename in modules_path.iterdir():
        if filename.suffix == ".py" and not filename.name.startswith("__"):
            module = f"bot.modules.{filename.stem}"
            try:
                await bot.load_extension(module)
                logger.info(f"✅ Loaded module: {module}")
            except Exception as e:
                logger.error(f"❌ Failed to load module {module}: {e}")

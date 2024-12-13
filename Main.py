import os
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_extensions():
    try:
        await bot.load_extension("bot.commands.ping")
        await bot.load_extension("bot.commands.grid")
        print("Extensions loaded successfully.")
    except Exception as e:
        print(f"Failed to load extension: {e}")

# Run everything once the bot is ready
@bot.event
async def on_ready():
    await load_extensions()

TOKEN = os.environ.get('TOKEN')
asyncio.run(bot.start(TOKEN))

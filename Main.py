import os
import discord
from discord.ext import commands

# Retrieve the token from environment variable
TOKEN = os.environ.get('TOKEN')

if not TOKEN:
    raise ValueError("The TOKEN environment variable is not set!")

# Intents configuration
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Simple load_extension
async def load_extensions():
    try:
        await bot.load_extension("bot.commands.ping")
        await bot.load_extension("bot.commands.grid")
        print("Extensions successfully loaded.")
    except Exception as err:
        print(f"Failed to load an extension: {err}")

@bot.event
async def on_ready():
    print(f"{bot.user.name} is now online!")
    await load_extensions()

bot.run(TOKEN)

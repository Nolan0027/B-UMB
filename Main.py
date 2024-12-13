import os
import random
import discord
from discord.ext import commands
import time

# Retrieve the token from environment variable
TOKEN = os.environ.get('TOKEN')

if not TOKEN:
    raise ValueError("The TOKEN environment variable is not set!")

# Intents configuration for the bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Properly create the bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

bot.run(TOKEN)

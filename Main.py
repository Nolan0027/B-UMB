import os
import discord
from discord.ext import commands

# Import commands dynamically
from bot.commands.ping import ping
from bot.commands.move import move
import time

# Define token
TOKEN = os.environ.get('TOKEN')

if not TOKEN:
    raise ValueError("The TOKEN environment variable is not set!")

bot_start_time = time.time()

# Bot setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# User data
bot.user_positions = {}

# Register commands
bot.command(name='ping')(ping)
bot.command(name='move')(move)

@bot.event
async def on_ready():
    print(f'Bot is online.')

bot.run(TOKEN)

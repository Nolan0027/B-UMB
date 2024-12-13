import os
import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load commands dynamically
bot.load_extension("bot.commands.ping")
bot.load_extension("bot.commands.grid")

TOKEN = os.environ.get('TOKEN')
bot.run(TOKEN)

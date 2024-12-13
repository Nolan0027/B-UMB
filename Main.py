import os
import discord
from discord.ext import commands
from Config import TOKEN
from bot.commands.move import move
from bot.commands.mine import mine
from bot.commands.reset import reset
from bot.commands.grid import grid
from bot.commands.list_commands import commands

# Intents configuration for the bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Register the commands
bot.add_command(move)
bot.add_command(mine)
bot.add_command(reset)
bot.add_command(grid)
bot.add_command(commands)

# Run the bot
bot.run(TOKEN)

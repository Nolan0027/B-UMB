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

bot = commands.Bot(command_prefix="!", intents=intents)

# Grid constants
GRID_WIDTH = 10
GRID_HEIGHT = 10

# User data
user_positions = {}
user_inventory = {}
chunks = {}
bot_start_time = time.time()

# Generate stones for a chunk
def generate_stones():
    stones_positions = set()
    for _ in range(10):  # Generate 10 stones per chunk
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        stones_positions.add((y, x))
    return stones_positions

# Get the current chunk
def get_current_chunk(user_id):
    position = user_positions.get(user_id, [0, 0])
    chunk_x, chunk_y = position[0] // GRID_HEIGHT, position[1] // GRID_WIDTH
    chunk_key = (chunk_x, chunk_y)

    if chunk_key not in chunks:
        chunks[chunk_key] = {"stones_positions": generate_stones()}
    return chunks[chunk_key]

# Display the grid
def display_grid(user_id):
    position = user_positions.get(user_id, [0, 0])
    px, py = position
    chunk = get_current_chunk(user_id)

    grid_lines = []
    stone_count = len(chunk["stones_positions"])

    for y in range(GRID_HEIGHT):
        row = []
        for x in range(GRID_WIDTH):
            if [y, x] == [px % GRID_HEIGHT, py % GRID_WIDTH]:
                row.append("P")  # Represent player
            elif (y, x) in chunk["stones_positions"]:
                row.append("S")
            else:
                row.append("g")
        grid_lines.append(" ".join(row))

    grid = "\n".join(grid_lines)
    stats = f"Player Position: {position} | Stones: {user_inventory.get(user_id, {'stones': 0})['stones']} | Grass: {GRID_WIDTH * GRID_HEIGHT - stone_count}"
    return f"{grid}\n{stats}"

# Ping and uptime command with processing time
@bot.command()
async def ping(ctx):
    try:
        start_time = time.time()

        latency = round(bot.latency * 1000)
        uptime = round(time.time() - bot_start_time)

        end_time = time.time()
        processing_time = round((end_time - start_time) * 1000)  # in milliseconds

        await ctx.send(f"Pong! Latency: {latency}ms | Uptime: {uptime} seconds | Processing Time: {processing_time}ms")

    except Exception as e:
        print(f"Error in ping command: {e}")
        await ctx.send("An error occurred while executing the ping command.")

# Move the player command
@bot.command()
async def move(ctx, direction=None):
    try:
        if direction is None:
            await ctx.send("Please specify a direction: `up`, `down`, `left`, or `right`")
            return

        user_id = ctx.author.id
        if user_id not in user_positions:
            user_positions[user_id] = [0, 0]

        position = user_positions.get(user_id, [0, 0])
        x, y = position

        if direction.lower() == "up":
            x -= 1
        elif direction.lower() == "down":
            x += 1
        elif direction.lower() == "left":
            y -= 1
        elif direction.lower() == "right":
            y += 1
        else:
            await ctx.send("Invalid direction! Use 'up', 'down', 'left', or 'right'.")
            return

        user_positions[user_id] = [x, y]
        grid_str = display_grid(user_id)
        await ctx.send(f"Moved {direction}!\n```\n{grid_str}\n```")

    except Exception as e:
        print(f"Error in move command: {e}")
        await ctx.send(f"An error occurred while moving: {str(e)}")

# Mine the stone command
@bot.command()
async def mine(ctx):
    try:
        user_id = ctx.author.id
        if user_id not in user_positions:
            user_positions[user_id] = [0, 0]

        position = user_positions.get(user_id, [0, 0])
        x, y = position
        chunk = get_current_chunk(user_id)

        ahead = (x % GRID_HEIGHT, (y + 1) % GRID_WIDTH)

        if ahead in chunk["stones_positions"]:
            chunk["stones_positions"].remove(ahead)

            inventory = user_inventory.get(user_id, {"stones": 0})
            inventory["stones"] += 1
            user_inventory[user_id] = inventory

            grid_str = display_grid(user_id)
            await ctx.send(
                f"Stone mined! Inventory: {inventory}\n```\n{grid_str}\n```"
            )
        else:
            await ctx.send("No stone ahead of the player.")

    except Exception as e:
        print(f"Error in mine command: {e}")
        await ctx.send(f"An error occurred while mining: {str(e)}")

# Reset the grid command
@bot.command()
async def reset(ctx):
    try:
        user_id = ctx.author.id
        user_positions[user_id] = [0, 0]
        user_inventory[user_id] = {"stones": 0}
        chunks.clear()  # Clear all chunk data
        generate_stones()

        grid_str = display_grid(user_id)
        await ctx.send(f"Grid reset!\n```\n{grid_str}\n```")

    except Exception as e:
        print(f"Error in reset command: {e}")
        await ctx.send("An error occurred while resetting the grid.")

# Commands list
@bot.command(aliases=["cmds"])
async def commands(ctx):
    try:
        commands_text = """
**Available Commands:**
- `!grid` - Display the current grid
- `!move <direction>` - Move the player in a specified direction (`up`, `down`, `left`, `right`)
- `!mine` - Mine a stone ahead of the player
- `!ping` - Check latency and uptime
- `!reset` - Reset the grid, regenerate new stones, and reset inventory
- `!commands` / `!cmds` - List all commands
"""
        await ctx.send(commands_text)

    except Exception as e:
        print(f"Error in commands list command: {e}")
        await ctx.send("An error occurred while listing commands.")

# Error handler to catch any unhandled exceptions
@bot.event
async def on_command_error(ctx, error):
    print(f"An error occurred in command {ctx.command}: {error}")
    await ctx.send(f"An error occurred while executing the command: {str(error)}")

# Run the bot
bot.run(TOKEN)

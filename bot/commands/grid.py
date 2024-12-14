import random
from discord.ext import commands

# Constants for the grid
GRID_WIDTH = 10
GRID_HEIGHT = 10

# User data
user_positions = {}
chunks = {}

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
    return f"```\n{grid}\n```"

async def setup(bot):
    @bot.command()
    async def grid(ctx):
        user_id = ctx.author.id

        # Initialize user position if not already set
        if user_id not in user_positions:
            user_positions[user_id] = [0, 0]

        grid_str = display_grid(user_id)
        await ctx.send(f"Here is your grid:\n{grid_str}")

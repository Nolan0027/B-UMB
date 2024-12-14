
Here's the complete implementation for the move command logic in a move.py file:

bot/commands/move.py
python
Copy code
from discord.ext import commands

# Constants for the grid
GRID_WIDTH = 10
GRID_HEIGHT = 10

# User data
user_positions = {}
chunks = {}

# Function to generate stones for a chunk
def generate_stones():
    stones_positions = set()
    for _ in range(10):  # Generate 10 stones per chunk
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        stones_positions.add((y, x))
    return stones_positions

# Function to get the current chunk
def get_current_chunk(user_id):
    position = user_positions.get(user_id, [0, 0])
    chunk_x, chunk_y = position[0] // GRID_HEIGHT, position[1] // GRID_WIDTH
    chunk_key = (chunk_x, chunk_y)

    if chunk_key not in chunks:
        chunks[chunk_key] = {"stones_positions": generate_stones()}
    return chunks[chunk_key]

# Function to display the grid
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
    async def move(ctx, direction=None):
        """Moves the player in the specified direction (up, down, left, or right)."""
        try:
            if direction is None:
                await ctx.send("Please specify a direction: `up`, `down`, `left`, or `right`.")
                return

            user_id = ctx.author.id

            # Initialize user position if not already set
            if user_id not in user_positions:
                user_positions[user_id] = [0, 0]

            position = user_positions.get(user_id, [0, 0])
            x, y = position

            # Handle direction input
            if direction.lower() == "up":
                x -= 1
            elif direction.lower() == "down":
                x += 1
            elif direction.lower() == "left":
                y -= 1
            elif direction.lower() == "right":
                y += 1
            else:
                await ctx.send("Invalid direction! Use `up`, `down`, `left`, or `right`.")
                return

            # Update user position
            user_positions[user_id] = [x, y]
            grid_str = display_grid(user_id)

            await ctx.send(f"Moved {direction}!\n{grid_str}")
        except Exception as e:
            print(f"Error in move command: {e}")
            await ctx.send(f"An error occurred while moving: {str(e)}")

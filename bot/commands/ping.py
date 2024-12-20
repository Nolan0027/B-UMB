import time
from discord.ext import commands

# This should be defined in Main.py to ensure it's globally accessible
bot_start_time = time.time()

async def ping(ctx):
    try:
        start_time = time.time()

        # Calculate latency in milliseconds
        latency = round(ctx.bot.latency * 1000)

        # Calculate uptime in seconds
        uptime = round(time.time() - bot_start_time)

        end_time = time.time()
        processing_time = round((end_time - start_time) * 1000)  # in milliseconds

        # Send the ping response
        await ctx.send(f"Pong! Latency: {latency}ms | Uptime: {uptime} seconds | Processing Time: {processing_time}ms")

    except Exception as e:
        print(f"Error in ping command: {e}")
        await ctx.send("An error occurred while executing the ping command.")

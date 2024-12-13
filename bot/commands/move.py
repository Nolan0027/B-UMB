from discord.ext import commands

async def move(ctx, direction=None):
    if direction is None:
        await ctx.send("Specify a direction: `up`, `down`, `left`, or `right`")
        return

    await ctx.send(f"Moving {direction}!")

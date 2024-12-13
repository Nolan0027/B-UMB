async def commands(ctx):
    available_commands = """
**Available Commands**
- !move <direction>: Move the player (`up`, `down`, `left`, `right`)
- !mine: Mine stone ahead
- !reset: Reset your game grid
- !grid: Show your game grid
- !cmds: List all available commands
"""
    await ctx.send(available_commands)

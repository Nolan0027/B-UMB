async def setup(bot):
    @bot.command()
    async def mine(ctx):
        """Mines a stone directly ahead of the player."""
        try:
            user_id = ctx.author.id

            # Ensure user has a position initialized
            if user_id not in user_positions:
                user_positions[user_id] = [0, 0]

            position = user_positions[user_id]
            x, y = position
            chunk = get_current_chunk(user_id)

            # Determine the position directly ahead of the player
            ahead = ((x % GRID_HEIGHT), (y + 1) % GRID_WIDTH)

            # Check if there is a stone in the position ahead
            if ahead in chunk["stones_positions"]:
                # Remove the stone from the chunk
                chunk["stones_positions"].remove(ahead)

                # Update the user's inventory
                inventory = user_inventory.get(user_id, {"stones": 0})
                inventory["stones"] += 1
                user_inventory[user_id] = inventory

                # Send feedback and updated grid
                grid_str = display_grid(user_id)
                await ctx.send(
                    f"Stone mined! Your inventory: {inventory}\n{grid_str}"
                )
            else:
                await ctx.send("No stone ahead to mine!")

        except Exception as e:
            print(f"Error in mine command: {e}")
            await ctx.send(f"An error occurred while mining: {str(e)}")

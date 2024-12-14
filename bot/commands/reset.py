async def setup(bot):
    @bot.command()
    async def reset(ctx):
        """Resets the grid, user position, inventory, and chunks."""
        try:
            user_id = ctx.author.id

            # Reset user-specific data
            user_positions[user_id] = [0, 0]
            user_inventory[user_id] = {"stones": 0}

            # Clear all chunks
            chunks.clear()

            # Re-generate stones for the initial chunk
            generate_stones()

            # Display the reset grid
            grid_str = display_grid(user_id)
            await ctx.send(f"Grid reset!\n{grid_str}")

        except Exception as e:
            print(f"Error in reset command: {e}")
            await ctx.send(f"An error occurred while resetting: {str(e)}")

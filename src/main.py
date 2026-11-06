import discord
from discord import app_commands
from discord.ext import commands
import logging
from pathlib import Path
import os


from Classes.myBot import MyBot
bot = MyBot()

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    logging.error(f"An error occurred: {error}")
    if isinstance(error, app_commands.CommandNotFound):
        await interaction.response.send_message("Command not found.")
    elif isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("You do not have permission to use this command.")
    else:
        await interaction.response.send_message(f"An unknown error occurred: {error}")

bot.run(os.getenv("DISCORD_BOT_TOKEN") or "No Token")
import discord
from discord import app_commands
from discord.ext import commands
import logging

from helpers import getMetadata
from databaseManager import DatabaseManager
from enums import *

metadata = getMetadata()

logHandler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode='w')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

databaseManager = DatabaseManager(databaseName = metadata["DBName"])

bot = commands.Bot(command_prefix="/", description="A2AS Personal Assistant", intents=intents)

@bot.event
async def on_ready():
    assert bot.user is not None
    try:
        synced = await bot.tree.sync()
        print(f"Synchronised {len(synced)} command(s).")
    except Exception as e:
        print(e)

@bot.tree.command(name="Manage")
@app_commands.describe()
async def manageTeam(interaction: discord.Interaction):

    team = databaseManager.getActiveTeamsByOwner(interaction.user.id)
    if not team:
        await interaction.response.send_message(embed=discord.Embed(
            title="You currently do not own any teams!",
            description="If this is an error, please contact the server owner."))
    else:
        await interaction.response.send_message(embed=discord.Embed(
            title="{0}".format(team["Name"])
        ))
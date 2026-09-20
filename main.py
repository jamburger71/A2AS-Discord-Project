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

@bot.tree.command(name="MyTeam")
@app_commands.describe()
async def myTeam(interaction: discord.Interaction):

    team = databaseManager.getOwnerTeam(interaction.user.id)
    
    if team == {}:
        interaction.respond.send_message("You don't own a team!")
    else:
        

@bot.tree.command(name="ChangeTeamName")
@app.commands.describe(newTeamName: str = "New Team Name")
async def changeTeamName(interaction: discord.Interaction, newTeamName: str):

    team = databaseManager.getOwnerTeam(interaction.user.id)
    if team == {}:
        #TODO

@bot.tree.command(name="Commands")
@app.commands.describe()
async def commands(interaction: discord.interaction):

    commandsEmbed = discord.Embed(
        title = "All Commands",
        description = "Below is a list of all available commands and a short description."
    )
    commandsEmbed.add_field(
        name = "Information Commands",
        value = """
        """,
        inline = False
    )
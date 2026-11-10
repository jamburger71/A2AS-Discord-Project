import discord
from discord import app_commands
from discord.ext import commands
import logging

from Classes.myBot import MyBot
from helpers import convertToPounds

class GenerateXML(commands.Cog):

    def __init__(self, bot: MyBot):
        self.bot = bot

    async def cog_load(self):
        logging.info(f"{self.__class__.__name__} command loaded successfully.")

    @app_commands.command(name="generatexml")
    @app_commands.describe()
    async def generatexml(self, interaction: discord.Interaction):

        await interaction.response.send_message("NOT DONE YET")

async def setup(bot: MyBot):  
    print("Loading GenerateXML cog...")
    await bot.add_cog(GenerateXML(bot))
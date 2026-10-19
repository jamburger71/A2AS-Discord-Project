import discord
from discord import app_commands
from discord.ext import commands
import logging

class GetTeams(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("GetTeams cog loaded successfully.")

    @app_commands.command(name="getteams")
    async def getteams(self, interaction: discord.Interaction):

        await interaction.response.send_message(self.bot.teamManager.getTeams())

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading GetTeams cog...")
    await bot.add_cog(GetTeams(bot))
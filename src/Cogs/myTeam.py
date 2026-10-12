import discord
from discord import app_commands
from discord.ext import commands
import logging

class MyTeam(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("MyTeam cog loaded successfully.")

    @app_commands.command(name="myteam")
    async def myteam(self, interaction: discord.Interaction):

        team: tuple | None = self.bot.teamManager.getOwnerTeam(interaction.user.id)
        
        if team is not None:
            logging.info(f"Team found for user {interaction.user.id}: {team[1]} (ID: {team[0]})")
            await interaction.response.send_message("Nice team bro")
        else:
            logging.info(f"No team found for user {interaction.user.id}")
            await interaction.response.send_message("You don't own a team!")

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading MyTeam cog...")
    await bot.add_cog(MyTeam(bot))
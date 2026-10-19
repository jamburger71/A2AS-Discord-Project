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

        print(interaction.user.id)
        team: tuple | None = self.bot.teamManager.getOwnerTeam(interaction.user.id)
        print(team)
        if team is None:
            logging.info(f"No team found for user {interaction.user.id}")
            await interaction.response.send_message("You don't own a team!")
            return
        logging.info(f"Team found for user {interaction.user.id}: {team[1]} (ID: {team[0]})")
        

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    logging.info("Loading MyTeam cog...")
    await bot.add_cog(MyTeam(bot))
import discord
from discord import app_commands
from discord.ext import commands
import logging

from areyousure import AreYouSure

class ChangeTeamName(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    async def cog_load(self):
        logging.info("ChangeTeamName cog loaded successfully.")

    @app_commands.command(name="changeteamname")
    @app_commands.describe(newteamname = "New Team Name")
    async def changeteamname(self, interaction: discord.Interaction, newteamname: str):

        team = self.bot.teamManager.getOwnerTeam(interaction.user.id)
        if team == None:
            await interaction.response.send_message("You don't own a team!")
        else:
            view = AreYouSure((team[0], newteamname), self.changeTeamNameConfirmed, await interaction.response.send_message("Team name change cancelled."))
            await interaction.response.send_message(embed = discord.Embed(
                title="Are you sure?", 
                description=f"You will be renaming your team from {team[1]} to {newteamname}. This action will have to be manually reverted."
                ), view=view)

    async def changeTeamNameConfirmed(self, args: tuple, interaction: discord.Interaction):
        teamID, newteamname = args
        self.bot.teamManager.updateTeamName(teamID, newteamname)
        await interaction.response.send_message(f"Team name changed to {newteamname}.")

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print("Loading ChangeTeamName cog...")
    await bot.add_cog(ChangeTeamName(bot))
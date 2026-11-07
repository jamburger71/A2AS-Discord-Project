import discord
from discord import app_commands
from discord.ext import commands
import logging

from Classes.myBot import MyBot
from Classes.team import Team

class RegisterTeamModal(discord.ui.Modal, title="Register Team"):

    def __init__(self, bot: MyBot):

        super().__init__()
        self.bot = bot
        
    name = discord.ui.TextInput(
        label="Team Name",
        placeholder="Team name...",
        required=True
    )
    description = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Team Description",
        placeholder = "Team description...",
        required=True,
        max_length=500
    )
    nationality = discord.ui.TextInput(
        label="Team Nationality",
        placeholder="Nationality...",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        
        teamID: int = self.bot.keyValManager.getAndIterateKeyVal("NextTeamID")
        startingCash: int = self.bot.keyValManager.getKeyVal("StartingCash")
        team: Team = Team.register(teamID, self.name.value, self.description.value, self.nationality.value, interaction.user.id, startingCash)
        self.bot.teamManager.insertTeam(team)
        await interaction.response.send_message("""Team Registered! Manage your team with /myteam.
        Until you have assigned your team a car, drivers, and an engine supplier, your team will not compete.
        You can assign these values using the commands in /myteam.""")
        self.bot.keyValManager.updateKeyVal("NextTeamID", teamID+1)

class RegisterTeam(commands.Cog):

    def __init__(self, bot: MyBot):  
        self.bot = bot

    async def cog_load(self):
        logging.info("RegisterTeam cog loaded successfully.")

    @app_commands.command(name="registerteam")
    @app_commands.describe()
    async def registerteam(self, interaction: discord.Interaction):
        team = self.bot.teamManager.getTeamByOwner(interaction.user.id)
        if team != None:
            await interaction.response.send_message("You already own a team! To manager your team, use /myteam")
            return
        await interaction.response.send_modal(RegisterTeamModal(bot=self.bot))

async def setup(bot: MyBot):  
    print("Loading RegisterTeam cog...")
    await bot.add_cog(RegisterTeam(bot))
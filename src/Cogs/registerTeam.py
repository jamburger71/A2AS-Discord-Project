import discord
from discord import app_commands
from discord.ext import commands
import logging

class RegisterTeam(commands.Cog):

    def __init__(self, bot: "MyBot"): # type: ignore
        self.bot = bot

    async def cog_load(self):
        logging.info("RegisterTeam cog loaded successfully.")

    @app_commands.command(name="registerteam")
    @app_commands.describe(
        teamname = "Team Name",
        teamnation = "Team Nation of Origin", 
        driver1 = "Driver 1 (by ID)", 
        driver2 = "Driver 2 (by ID)", 
        primarysponsor = "Primary Sponsor (by ID)",
        secondarysponsor1 = "Secondary Sponsor 1 (by ID)", 
        secondarysponsor2 = "Secondary Sponsor 2 (by ID)", 
        secondarysponsor3 = "Secondary Sponsor 3 (by ID)",
        enginesupplier = "Engine Supplier",
        tyremanufacturer = "Tyre Manufacturer"
    )
    async def registerteam(
        self,
        interaction: discord.Interaction, 
        teamname: str, 
        teamnation: str, 
        driver1: str, 
        driver2: str, 
        primarysponsor: str, 
        secondarysponsor1: str, 
        secondarysponsor2: str, 
        secondarysponsor3: str, 
        enginesupplier: str, 
        tyremanufacturer: str
    ):
        team = self.bot.teamManager.getOwnerTeam(interaction.user.id)
        if team != None:
            await interaction.response.send_message("You already own a team!")
        else:
            # Check if there are available team slots
            availableSlots = self.bot.teamManager.getAvailableTeamSlots(self.bot.keyValManager.getKeyVal("max_teams"))
            if availableSlots == 0:
                await interaction.response.send_message("No available team slots!")
            elif not self.bot.teamManager.tyreIsAvailable(tyremanufacturer):
                await interaction.response.send_message("The selected tyre manufacturer is not available!")
            elif driver1 == driver2:
                await interaction.response.send_message("You cannot select the same driver for both slots!")
            elif driver1 not in [driver[0] for driver in self.bot.driverManager.getAllDrivers(availableOnly=True)]:
                await interaction.response.send_message("The selected Driver 1 is not available!")
            elif driver2 not in [driver[0] for driver in self.bot.driverManager.getAllDrivers(availableOnly=True)]:
                await interaction.response.send_message("The selected Driver 2 is not available!")
            else:
                # Register the team
                teamID = self.bot.keyValManager.getKeyVal("NextTeamID")
                self.bot.teamManager.registerTeam(
                    interaction.user.id, 
                    teamname, 
                    teamnation, 
                    driver1, 
                    driver2, 
                    primarysponsor, 
                    secondarysponsor1, 
                    secondarysponsor2, 
                    secondarysponsor3, 
                    enginesupplier, 
                    tyremanufacturer,
                    teamID
                )
                self.bot.keyValManager.updateKeyVal("NextTeamID", teamID + 1)
                await interaction.response.send_message(embed = discord.Embed(
                    title=f"Team {teamname} registered successfully!",
                    description=f"You can check your team details at any time using the /myteam command."
                ))

async def setup(bot: "MyBot"): # type: ignore
    print("Loading RegisterTeam cog...")
    await bot.add_cog(RegisterTeam(bot))
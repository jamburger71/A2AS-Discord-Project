import discord
from discord import app_commands
from discord.ext import commands
import logging
import toml
from pathlib import Path

import helpers

LangDirectory = Path(__file__).resolve().parent.parent / "Resources" / "Locales"
print(LangDirectory)
with open("Eng.toml", 'r') as t:
    text = toml.load(t)

class InsertNewDriver(commands.Cog):
    
    def __init__(self, bot: "MyBot"): # type: ignore # noqa: F821
        self.bot = bot

    @app_commands.command(name="insertnewdriver", description="ADMIN ONLY: Insert a new driver into the database.")
    @app_commands.describe(
        drivername = "Driver First Name",
        lastname = "Driver Last Name",
        nationality = "Driver Nationality",
        age = "Driver Age",
        qualipace = "Qualifying Pace",
        racepace = "Race Pace",
        wetpace = "Wet Weather Pace",
        tyremanagement = "Tyre Management",
        aggressiveness = "Aggressiveness",
        defending = "Defending",
        contractcost = "Contract Cost"
    )
    @app_commands.checks.has_role("Moderator")
    async def insertnewdriver(
        self,
        interaction: discord.Interaction,
        drivername: str, 
        lastname: str,
        nationality: str, 
        age: int, 
        qualipace: int, 
        racepace: int,
        wetpace: int, 
        tyremanagement: int, 
        aggressiveness: int, 
        defending: int, 
        contractcost: int):
        if age < 18:
            logging.info(f"Failed to register driver {drivername} {lastname} - age {age} is below minimum.")
            await interaction.response.send_message(f"Driver age must be at least 18. Infants are not allowed.")
        elif not (0 <= qualipace <= 100):
            logging.info(f"Failed to register driver {drivername} {lastname} - qualifying pace {qualipace} is out of range.")
            await interaction.response.send_message(f"Qualifying pace must be between 0 and 100. Please try again.")
        elif not (0 <= racepace <= 100):
            logging.info(f"Failed to register driver {drivername} {lastname} - race pace {racepace} is out of range.")
            await interaction.response.send_message(f"Race pace must be between 0 and 100. Please try again.")
        elif not (0 <= wetpace <= 100):
            logging.info(f"Failed to register driver {drivername} {lastname} - wet weather pace {wetpace} is out of range.")
            await interaction.response.send_message(f"Wet weather pace must be between 0 and 100. Please try again.")
        elif not (0 <= tyremanagement <= 100):
            logging.info(f"Failed to register driver {drivername} {lastname} - tyre management {tyremanagement} is out of range.")
            await interaction.response.send_message(f"Tyre management must be between 0 and 100. Please try again.")
        elif not (0 <= aggressiveness <= 100):
            logging.info(f"Failed to register driver {drivername} {lastname} - aggressiveness {aggressiveness} is out of range.")
            await interaction.response.send_message(f"Aggressiveness must be between 0 and 100. Please try again.")
        elif not (0 <= defending <= 100):
            logging.info(f"Failed to register driver {drivername} {lastname} - defending {defending} is out of range.")
            await interaction.response.send_message(f"Defending must be between 0 and 100. Please try again.")
        else:
            
            threecode = helpers.getBestLetterCode(drivername, lastname, self.bot.driverManager.getAllThreeCodes())
            if threecode is not None:
                self.bot.driverManager.insertDriver(drivername, lastname, threecode, nationality, age, qualipace, racepace, wetpace, tyremanagement, aggressiveness, defending, contractcost)
                logging.info(f"Successfully registered driver {drivername} {lastname} with three-letter code {threecode}.")
                await interaction.response.send_message(f"{drivername} {lastname} has been registered successfully, with three-letter code {threecode}. You can check their stats at any time using the /getdriver command.")
            else:
                await interaction.response.send_message(f"Could not assign a valid Threecode to {drivername} {lastname}. Please try a different name.")
        

async def setup(bot: "MyBot"): # type: ignore # noqa: F821
    print(f"")
    await bot.add_cog(InsertNewDriver(bot))
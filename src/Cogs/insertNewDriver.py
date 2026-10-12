import discord
from discord import app_commands
from discord.ext import commands
import logging

class InsertNewDriver(commands.Cog):
    
    def __init__(self, bot: "MyBot"): # type: ignore
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
        if age < 16:
            logging.info(f"Failed to register driver {drivername} {lastname} - age {age} is below minimum.")
            await interaction.response.send_message(f"Driver age must be at least 16. Infants are not allowed.")
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
            noNameAvailable = False
            currentLastChar = 2
            currentMiddleChar = 1
            currentFirstChar = 0
            threecode = lastname[:3].upper()
            if self.bot.driverManager.getDriver(threecode) is not None and len(lastname) <= 3:
                noNameAvailable = True
            while self.bot.driverManager.getDriver(threecode) is not None and not noNameAvailable:
                threecode = f"{lastname[currentFirstChar]}{lastname[currentMiddleChar]}{chr(ord(lastname[currentLastChar]))}".upper()
                if currentMiddleChar < currentLastChar-1:
                    currentMiddleChar += 1
                elif currentLastChar < len(lastname)-1:
                    currentLastChar += 1
                    currentMiddleChar = currentFirstChar + 1
                elif currentFirstChar < len(lastname)-3:
                    currentFirstChar += 1
                    currentMiddleChar = currentFirstChar + 1
                    currentLastChar = currentMiddleChar + 1
                else:
                    noNameAvailable = True
            if noNameAvailable:
                logging.info(f"Failed to register driver {drivername} {lastname} - no three-letter code available.")
                await interaction.response.send_message(f"No available three-letter code for {drivername} {lastname}. Please try again with a different name.")
                return
            driverID = self.bot.keyValManager.getKeyVal("NextDriverID")
            self.bot.driverManager.insertDriver(driverID, drivername, lastname, threecode, nationality, age, qualipace, racepace, wetpace, tyremanagement, aggressiveness, defending, contractcost)
            self.bot.keyValManager.updateKeyVal("NextDriverID", driverID + 1)
            logging.info(f"Successfully registered driver {drivername} {lastname} with ID {driverID} and three-letter code {threecode}.")
            await interaction.response.send_message(f"{drivername} {lastname} has been registered successfully, with id {driverID} and three-letter code {threecode}. You can check his stats at any time using the /getdriver command.")

async def setup(bot: "MyBot"): # type: ignore
    print("Loading InsertNewDriver cog...")
    await bot.add_cog(InsertNewDriver(bot))
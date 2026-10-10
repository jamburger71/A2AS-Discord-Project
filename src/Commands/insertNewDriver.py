import discord
from discord import app_commands
from discord_ext import commands

@app_commands.command(name="insertnewdriver")
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
        await interaction.response.send_message(f"Driver age must be at least 16. Infants are not allowed.")
    elif not (0 <= qualipace <= 100):
        await interaction.response.send_message(f"Qualifying pace must be between 0 and 100. Please try again.")
    elif not (0 <= racepace <= 100):
        await interaction.response.send_message(f"Race pace must be between 0 and 100. Please try again.")
    elif not (0 <= wetpace <= 100):
        await interaction.response.send_message(f"Wet weather pace must be between 0 and 100. Please try again.")
    elif not (0 <= tyremanagement <= 100):
        await interaction.response.send_message(f"Tyre management must be between 0 and 100. Please try again.")
    elif not (0 <= aggressiveness <= 100):
        await interaction.response.send_message(f"Aggressiveness must be between 0 and 100. Please try again.")
    elif not (0 <= defending <= 100):
        await interaction.response.send_message(f"Defending must be between 0 and 100. Please try again.")
    else:
        noNameAvailable = False
        currentLastChar = 2
        currentMiddleChar = 1
        currentFirstChar = 0
        threecode = lastname[:3].upper()
        if driverManager.getDriver(threecode) is not None and len(lastname) <= 3:
            noNameAvailable = True
        while driverManager.getDriver(threecode) is not None and not noNameAvailable:
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
            await interaction.response.send_message(f"No available three-letter code for {drivername} {lastname}. Please try again with a different name.")
            return
        driverID = keyValManager.getKeyVal("NextDriverID")
        driverManager.insertDriver(driverID, drivername, lastname, threecode, nationality, age, qualipace, racepace, wetpace, tyremanagement, aggressiveness, defending, contractcost)
        keyValManager.updateKeyVal("NextDriverID", driverID + 1)
        await interaction.response.send_message(f"{drivername} {lastname} has been registered successfully, with id {driverID} and three-letter code {threecode}. You can check his stats at any time using the /getdriver command.")
            
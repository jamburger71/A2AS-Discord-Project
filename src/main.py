import discord
from discord import app_commands
from discord.ext import commands
import logging

from helpers import convertToPounds, groupReturnsByN
from databaseManager import DatabaseManager
from driverManager import DriverManager
from keyValManager import KeyValManager
from teamManager import TeamManager
from eventManager import EventManager
from enums import *
from areyousure import areYouSure
from pagecontroller import pagecontroller
import os
from dotenv import load_dotenv

load_dotenv()

logHandler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode='w')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

databaseManager = DatabaseManager(databaseName=os.getenv("DB_NAME"+".db") or "GenericDB.db")
driverManager = DriverManager(databaseManager.DatabaseConnection)
teamManager = TeamManager(databaseManager.DatabaseConnection)
eventManager = EventManager(databaseManager.DatabaseConnection)
keyValManager = KeyValManager(databaseManager.DatabaseConnection)

bot = commands.Bot(command_prefix="/", description="A2AS Personal Assistant", intents=intents)

@bot.event
async def on_ready():
    assert bot.user is not None
    try:
        synced = await bot.tree.sync()
        print(f"Synchronised {len(synced)} command(s).")
    except Exception as e:
        print(e)
    print("Ready to run!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to use this command.")
    else:
        await ctx.send(f"An error occurred: {error}")

@bot.tree.command(name="myteam")
@app_commands.describe()
async def myteam(interaction: discord.Interaction):

    team = teamManager.getOwnerTeam(interaction.user.id)
    
    if team == None:
        logging.info(f"No team found for user {interaction.user.id}")
        await interaction.response.send_message("You don't own a team!")
    else:
        logging.info(f"Team found for user {interaction.user.id}: {team}")
        await interaction.response.send_message("Nice team bro")

@bot.tree.command(name="changeteamname")
@app_commands.describe(newteamname = "New Team Name")
async def changeteamname(interaction: discord.Interaction, newteamname: str):

    team = teamManager.getOwnerTeam(interaction.user.id)
    if team == None:
        await interaction.response.send_message("You don't own a team!")
    else:
        view = areYouSure((team[0], newteamname), changeTeamName, await interaction.response.send_message("Team name change cancelled."), databaseManager)
        await interaction.response.send_message(embed = discord.Embed(
            title="Are you sure?", 
            description=f"You will be renaming your team from {team[1]} to {newteamname}. This action will have to be manually reverted."
            ), view=view)

async def changeTeamName(args: tuple, interaction: discord.Interaction, databaseManager: DatabaseManager):
    teamID, newteamname = args
    teamManager.updateTeamName(teamID, newteamname)
    await interaction.response.send_message(f"Team name changed to {newteamname}.")

@bot.tree.command(name="registerteam")
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
    team = teamManager.getOwnerTeam(interaction.user.id)
    if team != None:
        await interaction.response.send_message("You already own a team!")
    else:
        # Check if there are available team slots
        availableSlots = teamManager.getAvailableTeamSlots(keyValManager.getKeyVal("max_teams"))
        if availableSlots == 0:
            await interaction.response.send_message("No available team slots!")
        elif not teamManager.tyreIsAvailable(tyremanufacturer):
            await interaction.response.send_message("The selected tyre manufacturer is not available!")
        elif driver1 == driver2:
            await interaction.response.send_message("You cannot select the same driver for both slots!")
        elif driver1 not in [driver[0] for driver in driverManager.getAllDrivers(availableOnly=True)]:
            await interaction.response.send_message("The selected Driver 1 is not available!")
        elif driver2 not in [driver[0] for driver in driverManager.getAllDrivers(availableOnly=True)]:
            await interaction.response.send_message("The selected Driver 2 is not available!")
        else:
            # Register the team
            teamID = keyValManager.getKeyVal("NextTeamID")
            teamManager.registerTeam(
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
            keyValManager.updateKeyVal("NextTeamID", teamID + 1)
            await interaction.response.send_message(embed = discord.Embed(
                title=f"Team {teamname} registered successfully!",
                description=f"You can check your team details at any time using the /myteam command."
            ))

@bot.tree.command(name="transferownership")
@app_commands.describe(newowner = "New Owner (by Discord ID)")
async def transferownership(interaction: discord.Interaction, newowner: str):
    team = teamManager.getOwnerTeam(interaction.user.id)
    if team == None:
        await interaction.response.send_message("You don't own a team!")
    else:
        areYouSureView = areYouSure((team[0], newowner), changeTeamOwnership, dontChangeTeamOwnership, databaseManager)
        await interaction.response.send_message(embed = discord.Embed(
            title="Confirm Team Ownership Transfer",
            description=f"Are you sure you want to transfer ownership of team {team[1]} to {newowner}?"
        ), view=areYouSureView)

async def changeTeamOwnership(args: tuple, interaction: discord.Interaction, databaseManager: DatabaseManager):
    teamID, newOwnerID = args
    if not teamManager.checkIfUserOwnsTeam(newOwnerID):
        teamManager.changeTeamOwnership(teamID, newOwnerID)
    else:
        await interaction.response.send_message("That user already owns a team, and cannot own another.")

async def dontChangeTeamOwnership(args: tuple, interaction: discord.Interaction, databaseManager: DatabaseManager):
    await interaction.response.send_message("Team ownership transfer cancelled.")

@bot.tree.command(name="getdriver")
@app_commands.describe(driverid = "Driver ID or Three-Letter Code")
async def getdriver(interaction: discord.Interaction, driverid: str):
    if driverid.isdigit():
        driverid = int(driverid) # type: ignore
    driver = driverManager.getDriver(driverid)
    if driver is None:
        await interaction.response.send_message(f"No driver found with ID or code '{driverid}'.")
    else:
        driverEmbed = discord.Embed(title=f"{driver[1]} {driver[2]}")
        driverEmbed.description = f"ID: {driver[0]}\nNationality: {driver[4]}\nAge: {driver[5]}"
        driverEmbed.add_field(name="Stats", 
                              value=f"Qualifying Pace: {driver[6]}\nRace Pace: {driver[7]}\nWet Weather Pace: {driver[8]}\nTyre Management: {driver[9]}\nAggressiveness: {driver[10]}\nDefending: {driver[11]}", inline=False)
        driverEmbed.add_field(name="Contract Cost", value=convertToPounds(driver[12]))
        driverEmbed.add_field(name="Statistics",
                              value=f"Races: {driver[13]}\nWins: {driver[14]}\nPodiums: {driver[15]}", inline=False)
        await interaction.response.send_message(embed = driverEmbed)

@bot.tree.command(name="insertnewdriver")
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
        driverManager.insertDriver(drivername, lastname, threecode, nationality, age, qualipace, racepace, wetpace, tyremanagement, aggressiveness, defending, contractcost, driverID)
        keyValManager.updateKeyVal("NextDriverID", driverID + 1)
        await interaction.response.send_message(f"{drivername} {lastname} has been registered successfully.")
            
@bot.tree.command(name="removedriver")
@app_commands.describe(driverid = "Driver ID or Three-Letter Code")
@app_commands.checks.has_role("Moderator")
async def removedriver(interaction: discord.Interaction, driverid: str):
    if driverid.isdigit():
        driverid = int(driverid) # type: ignore
    driver = driverManager.getDriver(driverid)
    if driver is None:
        await interaction.response.send_message(f"No driver found with ID or code '{driverid}'.")
    else:
        view = areYouSure((driver,), removeDriverConfirmed, removeDriverCancelled, databaseManager)
        embed = discord.Embed(
            title="Are you sure?", 
            description=f"You will be removing {driver[1]} {driver[2]} from the database. You will need to manually re-insert him later if you want him back. This action cannot be undone.",
            )
        if not driverManager.checkDriverAvailability(driver[0]):
            embed.add_field(
                name="Warning", 
                value=f"This driver is currently contracted to a team."
            )
        await interaction.response.send_message(embed = embed, view=view)
            

async def removeDriverConfirmed(args: tuple, interaction: discord.Interaction, databaseManager: DatabaseManager):
    driver = args[0]
    driverManager.removeDriver(driver[0])
    await interaction.response.send_message(f"{driver[1]} {driver[2]} with ID {driver[0]} has been removed from the database.")

async def removeDriverCancelled(args: tuple, interaction: discord.Interaction, databaseManager: DatabaseManager):
    await interaction.response.send_message("Driver removal cancelled.")

@bot.tree.command(name="help")
@app_commands.describe()
async def help(interaction: discord.Interaction):

    commandsEmbed = discord.Embed(
        title = "All Commands",
        description = "Below is a list of all available commands and a short description."
    )
    commandsEmbed.add_field(
        name = "General Commands",
        value = """
        /help - Displays this help message
        /calendar - Displays the current season's calendar (NOT IMPLEMENTED)
        /standings - Displays the current season's standings (NOT IMPLEMENTED)
        /teamstandings - Displays the current season's team standings (NOT IMPLEMENTED)
        /alldrivers - Displays all drivers and their stats (NOT IMPLEMENTED)
        /viewprimarysponsors - Displays all primary sponsors and their stats (NOT IMPLEMENTED)
        /viewsecondarysponsors - Displays all secondary sponsors and their stats (NOT IMPLEMENTED)
        """,
        inline = False
    )
    commandsEmbed.add_field(
        name = "Team Management Commands",
        value = """
        /myteam - Displays your team information
        /changeteamname - Changes your team name
        /registerteam - Registers a new team.
        /transferownership - Transfers ownership of your team to another user. Tag the person you want to transfer ownership to. (NOT IMPLEMENTED)
        /buyupgrade - Buys an upgrade for your team (NOT IMPLEMENTED)
        """,
        inline = False
    )
    commandsEmbed.add_field(
        name = "Admin Commands (For Admins Only - duh)",
        value = """
        /removeteam - Removes a team from the database (NOT IMPLEMENTED)
        /agedrivers - Ages all drivers by 1 year, for use at the end of the season (NOT IMPLEMENTED)
        /createnewcalendar - Creates a new calendar for the next season (NOT IMPLEMENTED)
        /insertnewdriver - Inserts a new driver into the database (NOT IMPLEMENTED)
        /removedriver - Removes a driver from the database (NOT IMPLEMENTED)
        /changedrivername - Changes a driver's name (NOT IMPLEMENTED)
        /insertnewprimarysponsor - Inserts a new primary sponsor into the database (NOT IMPLEMENTED)
        """,
        inline = False
    )
    await interaction.response.send_message(embed = commandsEmbed)

@bot.tree.command(name="alldrivers")
@app_commands.describe(availableonly="Whether to only show available drivers")
async def alldrivers(interaction: discord.Interaction, availableonly: bool = False):
    drivers = driverManager.getAllDrivers(availableOnly=availableonly)
    if len(drivers) == 0:
        await interaction.response.send_message("No drivers found.")
    else:
        pages = groupReturnsByN(10, drivers)
        currentPage = 1
        embed = discord.Embed(title="All Drivers", description=f"Page {currentPage} of {len(pages)}")
        view = pagecontroller(pages=pages, currentPage=currentPage, interaction=interaction, nextPageFunc=nextPage)
        for driver in pages[currentPage - 1]:
            if driver is not None:
                embed.add_field(name=f"{driver[1]} {driver[2]}", value=f"ID: {driver[0]}, Code: {driver[3]}, Nationality: {driver[4]}, Age: {driver[5]}", inline=False)
        await interaction.response.send_message(embed=embed, view=view)

async def nextPage(interaction: discord.Interaction, lastMessage: discord.Message, pages: list, currentPage: int):
    totalPages = len(pages)
    embed = discord.Embed(title="All Drivers", description=f"Page {currentPage + 1} of {totalPages}")
    driverList = pages[currentPage]
    for driver in driverList:
        if driver is not None:
            embed.add_field(name=f"{driver[1]} {driver[2]}", value=f"ID: {driver[0]}, Code: {driver[3]}, Nationality: {driver[4]}, Age: {driver[5]}", inline=False)
    await lastMessage.delete()
    await interaction.response.send_message(embed=embed)

bot.run(os.getenv("DISCORD_BOT_TOKEN") or "No Token")
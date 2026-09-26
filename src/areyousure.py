import discord

from src.databaseManager import DatabaseManager

class areYouSure(discord.ui.View):
    def __init__(self, args: tuple, confirmFunc, denyFunc, databaseManager: DatabaseManager):
        super().__init__(timeout=60)
        self.args = args
        self.confirmFunc = confirmFunc
        self.denyFunc = denyFunc
        self.databaseManager = databaseManager

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.confirmFunc(args=self.args, interaction=interaction, databaseManager=self.databaseManager)
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.denyFunc is not None:
            await self.denyFunc(args=self.args, interaction=interaction, databaseManager=self.databaseManager)
        self.stop()
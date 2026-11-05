import discord

from Database.databaseManager import DatabaseManager

class AreYouSure(discord.ui.View):
    def __init__(self, confirmFunc, denyFunc):
        super().__init__(timeout=60)
        self.confirmFunc = confirmFunc
        self.denyFunc = denyFunc

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.confirmFunc(interaction=interaction)
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.denyFunc is not None:
            await self.denyFunc(interaction=interaction)
        self.stop()
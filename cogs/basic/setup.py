import discord
from discord import app_commands, ui
from discord.app_commands import Choice
from discord.ext import commands
from discord.ext import tasks
from scripts import frequency

class Setup(commands.Cog): #name of your cog class, typically name it based off of your .py file
    def __init__(self, client):
        self.client = client

    setupCmdGroup = app_commands.Group(name="setup", description="Commands related to changing your settings.")

    @setupCmdGroup.command(name="reminders", description="Change your reminder frequency.")
    async def reminders(self, interaction: discord.Interaction):
        flags = await frequency.checkFlags(7)
        await interaction.response.send_message(str(flags))


    @setupCmdGroup.command(name="courses", description="View courses attached to your user, so you may add them to this Guild.")
    async def server(self, interaction: discord.Interaction):
        user = False
        if user:
            await interaction.response.send_message("You are a user. I would show you the dropdown now.", ephemeral=True)
        else:
            await interaction.response.send_message("You are not a user. Please run </setup user:1141213429064011856> to add a Token to your account so I can access your available courses.", ephemeral=True)
        return
        
    @setupCmdGroup.command(name="user", description="Add a Canvas Token to your Discord User so we can access data like your courses and assignments.")
    async def user(self, interaction: discord.Interaction):
        return


async def setup(client: discord.Client):
    guild = client.get_guild(1038598934265864222) #uncomment this and the comment on line 18 to sync the cog to a specific guild
    await client.add_cog(Setup(client), guilds=[guild])
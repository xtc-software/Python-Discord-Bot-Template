import discord
from discord import app_commands, ui
from discord.app_commands import Choice
from discord.ext import commands
from discord.ext import tasks

global assignments
global assignmentChats
assignments = {}
assignmentChats = {}


class Study(commands.Cog): #name of your cog class, typically name it based off of your .py file
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="study", description="This is a command to find other uses looking to study for an assignment") #this is what names your command in the tree
    async def study(self, interaction: discord.Interaction, id: str): #function the command will perform
        check = assignments.get(id, False)
        if not check:
            assignments[id] = [interaction.user]
            await interaction.response.send_message("Currently no one is looking to study for this assignment yet. As soon as someone else tries to study this assignment, we will put you in a Group Chat.", ephemeral=True)
        elif check and interaction.user in check:
            check_2 = assignmentChats.get(id, False)
            if not check_2:
                guild = await self.client.fetch_guild(1038598934265864222)
                channel = await guild.create_text_channel(name=f"study-group-{id}")
                link = await channel.create_invite()
                assignmentChats[id] = channel.id
                await interaction.response.send_message(f"You're the first to the party! You can join the study group [here]({link.url}). The other user waiting for this study-group has been made aware and should join soon.", ephemeral=True)
            else:
                channel = await self.client.fetch_channel(assignmentChats[id])
                link = await channel.create_invite()
                await interaction.response.send_message(f"Looks like someone else is studying! You can join their study group [here]({link.url}).", ephemeral=True)
            studiers = assignments[id]
            assignments[id] = studiers.append(interaction.user)
            await interaction.response.send_message("I've added you to a Group Chat with the people studying for this!", ephemeral=True)
        #elif check and interaction.user in check:
        #    await interaction.response.send_message("Don't worry! We haven't forgot about you. Unfortunately there is still no one looking to study for this assignment. But if someone does, we will put you in a Group Chat as soon as possible.", ephemeral=True)
        #await interaction.response.send_message("You used the example cog!")
        return

async def setup(client):
    guild = client.get_guild(1038598934265864222) #uncomment this and the comment on line 18 to sync the cog to a specific guild
    await client.add_cog(Study(client), guilds=[guild])
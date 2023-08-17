import discord
from discord import app_commands, ui
from discord.app_commands import Choice
from discord.ext import commands
from discord.ext import tasks
import datetime
import asyncio
from scripts import db

global indexes
indexes = {}

class Backend(db.Database):
    async def getAssignments(self, userID: int = None, courseID: int = None):
        query = """
            SELECT * FROM assignments
            WHERE
                (userid = ? OR ? IS NULL) AND
                (courseid = ? OR ? IS NULL)
            ORDER BY due_at
            LIMIT 30
        """

        params = (userID, userID, courseID, courseID)

        try:
            db = await self.open()
            async with db.execute(query, params) as cursor:
                result = await cursor.fetchall()
            return result
        except Exception as e:
            return e
        finally:
            await self.close(db)

async def getAssignment(self, assignmentID):
    query = """
        SELECT * FROM assignments
        WHERE assignmentid = ?
    """
    params = (assignmentID,)

    try:
        db = await self.open()
        async with db.execute(query, params) as cursor:
            result = await cursor.fetchone()
        return result
    except Exception as e:
        return e
    finally:
        await self.close(db)

class Embeds():
    class Assignment(discord.Embed):
        async def build(id, name, description, due_date, allowed_extensions, points_possible, grading_type, index, count):
            embed = discord.Embed()
            embed.color = discord.Color.from_str("#E72429")
            embed.set_author(name=f"Assignment: {id}")
            embed.set_thumbnail(url="https://www.freeiconspng.com/thumbs/pencil-png/black-pencil-png-black-pencil-vector-8.png")
            embed.title = f"{name}"
            embed.description = description
            formats = ""
            for ext in allowed_extensions:
                formats = formats + f"{ext}\n"
            embed.add_field(name="File Formats", value=formats, inline=False)
            embed.add_field(name="Possible Points", value=points_possible, inline=False)
            embed.add_field(name="Grading Type", value=grading_type, inline=False)
            embed.add_field(name="Due Date", value=f"<t:{due_date}:R>")
            embed.set_footer(text=f"{index + 1} of {count}")
            return embed

class Views():
    class AssignmentOverview(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)    

    class AssignmentButtons(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
        
        @discord.ui.button(style=discord.ButtonStyle.gray, emoji="⏪")
        async def startButton(self, interaction: discord.Interaction, button: discord.ui.Button):
            indexes[interaction.user.id] = 0
            embed = await Embeds.Assignment.build("1234", "Math Test", "Chapter 4 Sections A-Z math test", "1692082800", [".txt", ".docx"], 100, "Flat", indexes[interaction.user.id], 5)
            await interaction.response.defer()
            await interaction.edit_original_response(embed=embed, view=Views.AssignmentButtons())
            return
        
        @discord.ui.button(style=discord.ButtonStyle.gray, emoji="⬅️")
        async def leftButton(self, interaction: discord.Interaction, button: discord.ui.Button):
            if indexes[interaction.user.id] > 0: 
                indexes[interaction.user.id] -= 1
            embed = await Embeds.Assignment.build("1234", "Math Test", "Chapter 4 Sections A-Z math test", "1692082800", [".txt", ".docx"], 100, "Flat", indexes[interaction.user.id], 5)
            await interaction.response.defer()
            await interaction.edit_original_response(embed=embed, view=Views.AssignmentButtons())
            return

        @discord.ui.button(style=discord.ButtonStyle.green, label="Turn In", emoji="📝")
        async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
            time = datetime.datetime.now()
            future = time + datetime.timedelta(seconds=30)
            future = future.timestamp()
            future = round(future)
            await interaction.response.send_message(f"Please upload a file via Discord Attachments <t:{future}:R>")
            await asyncio.sleep(30)
            attachment = None
            async for message in interaction.channel.history(limit=1):
                if len(message.attachments) > 0: 
                    attachment = message.attachments[0].url
            if attachment is None:
                await interaction.edit_original_response(content="Time expired for upload. Please use the command again.")
            else:
                await interaction.edit_original_response(content=f"Your file is located at: {attachment}")
            return
        
        @discord.ui.button(style=discord.ButtonStyle.gray, emoji="➡️")
        async def rightButton(self, interaction: discord.Interaction, button: discord.ui.Button):
            lastAssignment = 5
            if indexes[interaction.user.id] + 1 < lastAssignment:
                indexes[interaction.user.id] += 1
            embed = await Embeds.Assignment.build("1234", "Math Test", "Chapter 4 Sections A-Z math test", "1692082800", [".txt", ".docx"], 100, "Flat", indexes[interaction.user.id], 5)
            await interaction.response.defer()
            await interaction.edit_original_response(embed=embed, view=Views.AssignmentButtons())
            return
        
        @discord.ui.button(style=discord.ButtonStyle.gray, emoji="⏩")
        async def endButton(self, interaction: discord.Interaction, button: discord.ui.Button):
            indexes[interaction.user.id] = 4
            embed = await Embeds.Assignment.build("1234", "Math Test", "Chapter 4 Sections A-Z math test", "1692082800", [".txt", ".docx"], 100, "Flat", indexes[interaction.user.id], 5)
            await interaction.response.defer()
            await interaction.edit_original_response(embed=embed, view=Views.AssignmentButtons())
            return

class Assignments(commands.Cog): #name of your cog class, typically name it based off of your .py file
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="assignments", description="This is a command to view assignments available to you.") #this is what names your command in the tree
    async def assignments(self, interaction: discord.Interaction): #function the command will perform
        if interaction.guild is not None: #check if we are in a dm
            await interaction.response.send_message("This command is only available in Direct Messages.", ephemeral=True) 
            return
        indexes[interaction.user.id] = 0
        embed = await Embeds.Assignment.build("1234", "Math Test", "Chapter 4 Sections A-Z math test", "1692082800", [".txt", ".docx"], 100, "Flat", indexes[interaction.user.id], 5)
        await interaction.response.send_message(embed=embed, view=Views.AssignmentButtons(), ephemeral=True)
        


async def setup(client):
    #guild = client.get_guild(1038598934265864222) #uncomment this and the comment on line 18 to sync the cog to a specific guild
    await client.add_cog(Assignments(client))#, guilds=[guild])
import discord
from discord.ext import commands

class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.has_permissions(administrator=True)  # ensure only admins can run this
    async def channel(self, ctx, channel_name: str):
        # Check if channel with this name already exists
        existing_channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
        if existing_channel:
            await ctx.send(f"A channel with the name {channel_name} already exists!")
            return

        # Create a new text channel
        new_channel = await ctx.guild.create_text_channel(name=channel_name)
        
        # Store the new channel ID and name in the database
        # ... (DB code to insert new channel data)

        await ctx.send(f"Channel {new_channel.mention} created and configured for the !create command!")

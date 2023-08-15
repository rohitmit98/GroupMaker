import discord
from discord.ext import commands
from config import ACTIVE_GROUP_CHANNEL

class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def create(self, ctx, group_type: str, group_name, *, content: str = ""):
        global active_group_channel
        global role_specific_channel
        target_channel = ctx.guild.get_channel(active_group_channel)

        # if no content to post / accidental "enter" pressed 
        if (group_type != "study" or group_type != "project"):
            empty_content_msg = await ctx.send("Process Failed. Please provide a valid group type.", allowed_mentions=no_notification)
            await ctx.message.delete(delay=5)
            await empty_content_msg.delete(delay=10)

        # if no content to post / accidental "enter" pressed 
        elif (not group_name):
            empty_content_msg = await ctx.send("Process Failed. Please provide a valid group name.", allowed_mentions=no_notification)
            await ctx.message.delete(delay=5)
            await empty_content_msg.delete(delay=10)
        # if no content to post / accidental "enter" pressed 
        elif (not content):
            empty_content_msg = await ctx.send("Process Failed. Please provide group content. What are you creating?", allowed_mentions=no_notification)
            await ctx.message.delete(delay=5)
            await empty_content_msg.delete(delay=10)

        else: 
            # Check if group_name already exists, if so, append # to it 
            existing_role = discord.utils.get(ctx.guild.roles, name=group_name)
            counter = 1
            original_group_name = group_name
            if existing_role: 
                while (existing_role): 
                    group_name = f"{original_group_name}{counter}"  # append counter to original name
                    existing_role = discord.utils.get(ctx.guild.roles, name=group_name)  # check again
                    counter += 1  # increment counter for next iteration if needed
                    
            # create standard learning group message 
            if (group_type == "study"):
                intro_msg = (
                f"## Study Group: {group_name} \n"
                f"Welcome to the {group_name} Study Group! "
                "If you're excited to join this study, give this a 👍 reaction. "
                "Reacting will assign you a specific role and grant you access to our group text channel. \n\n"
                f"{content}\n\n"
                f"Created by User: {ctx.author.mention}"
                )
            elif (group_type == "project"):
                intro_msg = (
                f"## Project Group: {group_name} \n"
                f"Welcome to the {group_name} Project Group! "
                "If you're excited to join this project, give this a 👍 reaction. "
                "Reacting will assign you a specific role and grant you access to our group text channel. \n\n"
                f"{content}\n\n"
                f"Created by User: {ctx.author.mention}"
                )

            # send message to #active-learning-groups channel
            intro_msg_object = await target_channel.send(content=intro_msg, embed=None)
            

            await intro_msg_object.add_reaction("👍")
            await ctx.message.delete(delay=5)
            # send the bot's member count message
            member_count_msg = "👥 **Current Member Count:** 1"
            member_count_obj = await target_channel.send(member_count_msg, allowed_mentions=no_notification)

            # store intro_message into dictionary with unique {group_name, member_count_obj} pair
            intro_messages[intro_msg_object.id] = (group_name,member_count_obj.id)

            # create a new role with group_name
            try:
                new_role = await ctx.guild.create_role(name=group_name, reason="Created for new learning group.")
                new_role_msg = await ctx.send(f"Role {new_role.name} created successfully!", allowed_mentions=no_notification)
                await new_role_msg.delete(delay=5)
            except discord.errors.Forbidden:
                new_role_forbid = await ctx.send("I don't have permissions to create roles!", allowed_mentions=no_notification) 
                await new_role_forbid.delete(delay=5)
            except discord.HTTPException as e:
                new_role_fail = await ctx.send(f"Failed to create role: {e}", allowed_mentions=no_notification)
                await new_role_fail.delete(delay=5)

            # assign user who used command with role 
            try:
                await ctx.author.add_roles(new_role, reason="Assigned role for new learning group.")
                role_assign_msg = await ctx.send(f"Assigned {new_role.name} to {ctx.author.display_name}!", allowed_mentions=no_notification)
                await role_assign_msg.delete(delay=5)
            except discord.errors.Forbidden:
                role_assign_forbid = await ctx.send("I don't have permissions to assign roles!", allowed_mentions=no_notification)
                await role_assign_forbid.delete(delay=5)
            except discord.HTTPException as e:
                role_assign_fail = await ctx.send(f"Failed to assign role: {e}", allowed_mentions=no_notification)
                await role_assign_fail.delete(delay=5)

            # create a new channel with group_name inside category
            category_id = role_specific_channel
            category = ctx.guild.get_channel(category_id)
            if not category:
                category_fail = await ctx.send("Failed to find the category!", allowed_mentions=no_notification)
                return
            
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                new_role: discord.PermissionOverwrite(read_messages=True)
            }
            
            try:
                new_channel = await ctx.guild.create_text_channel(name=group_name, category=category, overwrites=overwrites)
                new_channel_msg = await ctx.send(f"Channel {new_channel.mention} created under {category.name} category!", allowed_mentions=no_notification)
                await new_channel_msg.delete(delay =5)
            except discord.errors.Forbidden:
                new_channel_forbid = await ctx.send("I don't have permissions to create channels!", allowed_mentions=no_notification)
                new_channel_forbid.delete(delay=5)
            except discord.HTTPException as e:
                new_channel_fail = await ctx.send(f"Failed to create channel: {e}", allowed_mentions=no_notification)
                new_channel_fail.delete(delay=5)

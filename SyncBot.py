import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()


    intents = discord.Intents.default()  # This will enable all default intents
    intents.members = True  # This will enable the members intent which is off by default
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'We have logged in as {bot.user.name}')

    # store all intro_messages into dictionary for access 
    intro_messages = {}
    active_learning_id = 1139164829479862324
    role_specific_id = 1139037091733438495
    no_notification = discord.AllowedMentions.none()

    @bot.command()
    async def create(ctx, group_name: str, *, content: str = ""):
        global active_learning_id
        global role_specific_id
        target_channel = ctx.guild.get_channel(active_learning_id)

        # if no content to post / accidental "enter" pressed 
        if (not content):
            empty_content_msg = await ctx.send("Proccess Failed. Please provide self-study content.", allowed_mentions=no_notification)
            await ctx.message.delete(delay=5)
            await empty_content_msg.delete(delay=5)

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
            intro_msg = (
            f"## Learning Group: {group_name} \n"
            f"Welcome to the {group_name} Learning Group! "
            "If you're excited to join this self-study, give this a 👍 reaction. "
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
            category_id = role_specific_id
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

    @bot.event
    async def on_raw_reaction_add(payload):
        global intro_messages
        global active_learning_id

        if payload.channel_id != active_learning_id:
            return 
        
        # Check if the reaction is on an intro message
        channel = bot.get_channel(payload.channel_id)
        group_name, member_count_id = intro_messages.get(payload.message_id, (None, None))
        if group_name and payload.emoji.name == "👍":
            guild = bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)

            role = discord.utils.get(guild.roles, name=group_name)
            if role:
                await user.add_roles(role)
                new_role_msg = await channel.send(f"{user.mention} has been successfully assigned role {role}!", allowed_mentions=no_notification)
                await new_role_msg.delete(delay=5)


            
            # Increment member count
            member_count_channel = bot.get_channel(active_learning_id)
            member_count_msg = await member_count_channel.fetch_message(member_count_id)
            current_count = int(member_count_msg.content.split()[-1])  # assuming the message ends with the count
            new_count = current_count + 1
            await member_count_msg.edit(content=f"👥 **Current Member Count:** {new_count}")

    @bot.event
    async def on_raw_reaction_remove(payload):
        global intro_messages
        global active_learning_id

        channel_id = payload.channel_id
        if channel_id != active_learning_id:
            return 

        # Check if the reaction is on an intro message
        channel = bot.get_channel(payload.channel_id)
        group_name, member_count_id = intro_messages.get(payload.message_id, (None, None))
        if group_name and payload.emoji.name == "👍":
            guild = bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)

            role = discord.utils.get(guild.roles, name=group_name)
            if role:
                await user.remove_roles(role)
                new_role_msg = await channel.send(f"{user.mention} has been successfully removed role {role}!", allowed_mentions=no_notification)
                await new_role_msg.delete(delay=5)

            # Decrement member count
            member_count_channel = bot.get_channel(active_learning_id)
            member_count_msg = await member_count_channel.fetch_message(member_count_id)
            current_count = int(member_count_msg.content.split()[-1])  # assuming the message ends with the count
            new_count = current_count - 1
            await member_count_msg.edit(content=f"👥 **Current Member Count:** {new_count}")

    bot.run('MTEzOTUxOTA1MDM1NjExNzU2NQ.G_yuUr.AZex8N-RF4joZBM8joSjpjS4VRlDMK5T-m3es8')  

    # Current Token: MTEzOTUxOTA1MDM1NjExNzU2NQ.G_yuUr.AZex8N-RF4joZBM8joSjpjS4VRlDMK5T-m3es8
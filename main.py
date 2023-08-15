import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import psycopg2
from config import BOT_TOKEN 

conn = psycopg2.connect(
    dbname="groupmakerdb",
    user="username",
    password="password",
    host="150.136.87.39",
    port="5432"  # default port for Postgres, change if yours is different
)

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
    async def on_ready():
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!help for commands"))
        print(f'We have logged in as {bot.user.name}')

    # store all intro_messages into dictionary for access 
    intro_messages = {}
    active_group_channel = 1139164829479862324
    role_specific_channel = 1139037091733438495
    no_notification = discord.AllowedMentions.none()


    @bot.event
    async def on_raw_reaction_add(payload):
        global intro_messages
        global active_group_channel

        if payload.channel_id != active_group_channel:
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
            member_count_channel = bot.get_channel(active_group_channel)
            member_count_msg = await member_count_channel.fetch_message(member_count_id)
            current_count = int(member_count_msg.content.split()[-1])  # assuming the message ends with the count
            new_count = current_count + 1
            await member_count_msg.edit(content=f"👥 **Current Member Count:** {new_count}")

    @bot.event
    async def on_raw_reaction_remove(payload):
        global intro_messages
        global active_group_channel

        channel_id = payload.channel_id
        if channel_id != active_group_channel:
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
            member_count_channel = bot.get_channel(active_group_channel)
            member_count_msg = await member_count_channel.fetch_message(member_count_id)
            current_count = int(member_count_msg.content.split()[-1])  # assuming the message ends with the count
            new_count = current_count - 1
            await member_count_msg.edit(content=f"👥 **Current Member Count:** {new_count}")

    bot.run(BOT_TOKEN)  
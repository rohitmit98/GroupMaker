import discord
from discord.ext import bridge
from discordToken import BOT_TOKEN
from database.queries import insert_server_data, delete_server_data

bot = bridge.Bot(command_prefix='!', intents=discord.Intents.all(), auto_sync_commands=True)


@bot.event
async def on_ready():
    print(f"Ready - this bot is owned by {bot.user}")


@bot.event
async def on_guild_join(guild):
    # print(f"Guild joined: {guild.name}")
    insert_server_data(guild.id)


@bot.event
async def on_guild_remove(guild):
    # print(f"Guild left: {guild.name}")
    delete_server_data(guild.id)


async def main():
    bot.load_extension("cogs.create_command")
    bot.load_extension("cogs.disband_command")
    await bot.start(BOT_TOKEN)


loop = bot.loop
loop.run_until_complete(main())

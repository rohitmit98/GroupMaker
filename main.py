import discord
from discord.ext import bridge
from database.connect import db_pool
from discordToken import BOT_TOKEN

bot = bridge.Bot(command_prefix='!', intents=discord.Intents.all(), auto_sync_commands=True)


# Function to insert guild_id, and timestamp for joined into 'servers' Table
def insert_server_data(guild_id: int):
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO guilds (guild_id, join_date) VALUES (%s, CURRENT_TIMESTAMP) ON CONFLICT DO NOTHING;",
                (guild_id,))
            conn.commit()
    finally:
        db_pool.putconn(conn)


def delete_server_data(guild_id: int):
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM guilds WHERE guild_id = %s;", (guild_id,))
            conn.commit()
    finally:
        db_pool.putconn(conn)


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

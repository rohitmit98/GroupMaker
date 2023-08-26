import discord
from typing import Union
from database.connect import db_pool


async def add_category(guild_id: int, category_id: int, category_name: str, post_channel_id: int, emoji: str,
                       admin_msg: str):
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO group_categories (guild_id, category_id, category_name, post_channel_id, emoji, admin_msg) 
                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
                """,
                (guild_id, category_id, category_name, post_channel_id, emoji, admin_msg)
            )
            conn.commit()
    finally:
        db_pool.putconn(conn)


async def remove_category(guild_id: int, category_id: int):
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM group_categories WHERE (guild_id = %s AND category_id = %s);
                """,
                (guild_id, category_id)
            )
            conn.commit()
    finally:
        db_pool.putconn(conn)


async def get_category_id_from_name(guild_id: int, category_name: str):
    """
     Fetches category id for a given category name.

     :param category_name: The name of a Guild Category (str)
     :param guild_id: A Guild ID (int)
     :return: A category id.
     """
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT category_id FROM group_categories WHERE guild_id = %s AND category_name = %s",
                           (guild_id, category_name))
            id_ = cursor.fetchone()
            if id_:
                return id_[0]
    finally:
        db_pool.putconn(conn)
    return None  # or raise an exception, or handle this case however you prefer


async def get_category_names(guild: Union[int, discord.Guild]):
    """
     Fetches category names for a given guild.

     :param guild: Either a Guild ID (int) or a Discord Guild object.
     :return: List of category names.
     """
    names = []

    guild_id = guild.id if isinstance(guild, discord.Guild) else guild

    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            # execute SELECT query
            cursor.execute("SELECT category_name, emoji FROM group_categories WHERE guild_id = %s", (guild_id,))

            # fetch all results
            rows = cursor.fetchall()

            for rows in rows:
                names.append(f"{rows[0]} {rows[1]}")
    finally:
        db_pool.putconn(conn)

    return names


async def get_category_names_autocomplete(ctx: discord.AutocompleteContext):
    return await get_category_names(ctx.interaction.guild)


def add_group(guild_id: int, category_id: int, group_owner_id: int, post_id: int, text_channel_id: int,
              voice_channel_id: int):
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO groups (guild_id, category_id, group_owner_id, post_id, text_channel_id, voice_channel_id, form_date) 
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP) ON CONFLICT DO NOTHING;
                """,
                (guild_id, category_id, group_owner_id, post_id, text_channel_id, voice_channel_id)
            )
            conn.commit()
    finally:
        db_pool.putconn(conn)

import emoji
import discord

# Unicode Emojis
all_emojis = emoji.EMOJI_DATA


async def emoji_autocomplete(ctx: discord.AutocompleteContext):
    guild = ctx.interaction.guild
    user_input = ctx.value.lower()
    matching_emojis = []

    for emoji_char, alias in all_emojis.items():
        alias_name = alias.get('en', '').lower()  # added .lower()
        if alias_name and user_input in alias_name:
            matching_emojis.append(emoji_char)

    return matching_emojis[:10]

#
# # getting custom emojis from server
# matching_custom_emojis = [str(guild_emoji) for guild_emoji in guild.emojis if ctx.value.lower() in guild_emoji.name.lower()]
# matching_emojis.extend(matching_custom_emojis)

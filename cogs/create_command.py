from discord.commands import option
from discord.ext import bridge, commands
from helpers.emoji_helper import emoji_autocomplete
from database.queries import add_category
import emoji


class CreateCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # DISCORD COMMAND GROUP "/CREATE"
    @bridge.bridge_group()
    async def create(self, ctx: bridge.BridgeContext):
        # This will be the default behavior if someone just invokes '/create'
        # If not needed, you can keep it empty or provide some help message.
        await ctx.respond("Use a subcommand of create, e.g., '/create category'.")

    # DISCORD SUBCOMMAND "/CREATE GROUP"
    @create.command(description="Create a GroupMaker category for your server!")
    @option(
        name="category-name",
        parameter_name="category_name",
        description="What type of category is this group (i.e. project)?",
        required=True,
    )
    @option(
        name="emoji",
        parameter_name="emoji_char",
        autocomplete=emoji_autocomplete,
        description="Whats a suitable emoji representation for this category? default=👍",
        required=True
    )
    @option(
        name="admin-msg",
        parameter_name="admin_msg",
        description="Do you have a message you'd like to include for posts with this category? default=\"\"",
        required=False
    )
    @option(
        name="public",
        parameter_name="public_str",
        description="Do you want this message to be viewable for everyone?",
        choices=["True", "False"],
        required=False
    )
    async def category(self, ctx: bridge.BridgeContext,
                       category_name: str,
                       emoji_char: str,
                       admin_msg: str = "",
                       public_str: str = "False"):

        public_bool = False
        if public_str == "True":
            public_bool = True

        # Check if existing category
        existing_discord_categories = [cat.name for cat in ctx.guild.categories]
        if category_name in existing_discord_categories:
            response_message = "Warning: Duplicate category name in Discord server!"
            public_bool = False

        elif not emoji.purely_emoji(emoji_char):
            response_message = "Please choose an emoji from the dropdown."

        else:
            # Create the new category
            new_category = await ctx.guild.create_category(f"{category_name} {emoji_char}")

            # # create a "#find-groups" text channel, where users post will go
            new_channel = await ctx.guild.create_text_channel(name="find-groups", category=new_category)

            # Once the category is created, update your database
            await add_category(ctx.guild.id, new_category.id, category_name, new_channel.id, emoji_char,
                               admin_msg)
            await ctx.defer()

            response_message = (f"Successfully added group category **\"{new_category}\"** in Server.\n\n"
                                f"**Group myformations for this category will post in channel:** <#{new_channel.id}>\n\n"
                                f"{'**Standard admin message for every post:** ' + admin_msg if admin_msg.strip() != '' else ''}")

        await ctx.respond(response_message, ephemeral=not public_bool)


def setup(bot):
    bot.add_cog(CreateCommand(bot))

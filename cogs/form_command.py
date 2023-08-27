from discord.commands import option
from discord.ext import bridge, commands
from database.queries import add_group, get_category_names_autocomplete, get_category_id_from_name


# @commands.has_permissions(administrator=True)
class FormCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # DISCORD COMMAND GROUP "/CREATE"
    @bridge.bridge_group()
    async def form(self, ctx: bridge.BridgeContext):
        # This will be the default behavior if someone just invokes '/create'
        # If not needed, you can keep it empty or provide some help message.
        await ctx.respond("Use a subcommand of form, e.g., '/form group'.")

    @form.command(description="Form a group using GroupMaker in this server!")
    @option(
        name="group-type",
        parameter_name="group_type",
        description="Which group category do you want to delete?",
        autocomplete=get_category_names_autocomplete,
        required=True
    )
    @option(
        name="group-type",
        parameter_name="category_name",
        description="What would you like to name your group?",
        required=True
    )
    @option(
        name="group-name",
        parameter_name="group_name",
        description="What would you like to name your group?",
        required=True
    )
    @option(
        name="post-title",
        parameter_name="post_title",
        description="What will be the title of your group post?",
        required=True
    )
    @option(
        name="post-content",
        parameter_name="post_content",
        description="Add some content here that describes your group.",
        required=True
    )
    @option(
        name="emoji",
        parameter_name="emoji",
        description="Would you like to specify an reaction emoji for your post?",
        required=False
    )
    async def group(self, ctx: bridge.BridgeContext,
                    category_name: str,
                    group_name: str,
                    post_title: str,
                    post_content: str,
                    emoji: str):
        category_id = await get_category_id_from_name(category_name)
        # use (guild_id, category_id) to find relevant information from group_categories: post_channel_id, emoji, and admin_msg
        # if no emoji specified, use emoji admin set for the group-type

        # Add a row in groups using add_group

        # make a post formatted:
        # ## Post_Title
        # *bold-italics* admin_msg
        # ### React with {emoji} to join this group!
        # Group By: {user}


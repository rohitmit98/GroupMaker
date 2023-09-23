import discord
from discord import ui
from discord.commands import option
from discord.ext import bridge, commands
from database.queries import remove_category, get_category_id_from_name, get_category_names_autocomplete


class DisbandCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_group()
    async def disband(self, ctx: bridge.BridgeContext):
        # This will be the default behavior if someone just invokes '/create'
        # If not needed, you can keep it empty or provide some help message.
        await ctx.respond("Use a subcommand of disband, e.g., '/disband category'.")

    @disband.command(description="Disband a group or category from your server.")
    @option(
        name="category-name",
        parameter_name="category_name",
        description="Which group category do you want to delete?",
        autocomplete=get_category_names_autocomplete,
        required=True
    )
    async def category(self, ctx: bridge.BridgeContext, category_name: str):
        category_str = category_name[:-2]

        category_id = await get_category_id_from_name(ctx.guild.id, category_str)

        # Create the confirmation view with buttons
        view = ConfirmationButton(ctx, category_id)

        # Send a message with the confirmation buttons
        await ctx.respond(
            f"⚠️**WARNING:** Are you **sure** you want to disband the category: {category_name} ? "
            f"This will effectively **ERASE ALL** the channel data within the category. ⚠️",
            ephemeral=True, view=view)


class ConfirmationButton(ui.View):
    def __init__(self, ctx, category_id):
        super().__init__()
        self.ctx = ctx
        self.category_id = category_id

    @ui.button(label='Yes', style=discord.ButtonStyle.success)
    async def confirm(self, button: ui.Button, interaction: discord.Interaction):
        # delete yes/no button message
        await self.message.delete(delay=3)

        # proceed deleting rest of category and channels
        category_channel = self.ctx.guild.get_channel(self.category_id)
        for channel in category_channel.channels:
            await channel.delete()

        if isinstance(category_channel, discord.CategoryChannel):
            await category_channel.delete()

        await remove_category(interaction.guild.id, category_channel.id)

        await interaction.response.send_message(f"Successfully removed category {category_channel.name} from Server.",
                                                ephemeral=True)
        self.stop()

    @ui.button(label='No', style=discord.ButtonStyle.danger)
    async def cancel(self, button: ui.Button, interaction: discord.Interaction):
        # delete yes/no button message
        await self.message.delete(delay=3)

        await interaction.response.send_message("Category deletion cancelled.",
                                                ephemeral=True)
        self.stop()


def setup(bot):
    bot.add_cog(DisbandCommand(bot))

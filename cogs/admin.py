"""Cogs for admin features"""
from discord.ext import commands


class Admin(commands.Cog, name="Admin"):
    """Cogs for admin commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reload-extension", help="reloads <extension>")
    @commands.has_role("Moderator")
    async def reload_extension(self, ctx: commands.Context, extension: str):
        """reload_extension
        ---

        Command that reloads an extension.

        Arguments:
            ctx {discord.ext.commands.Context} -- Context of the command.
            extension {str} -- extension to reload
        """
        self.bot.reload_extension(extension)
        await ctx.send("Extension reloaded")


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(Admin(bot))

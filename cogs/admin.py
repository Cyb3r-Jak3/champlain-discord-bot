"""Cogs for admin features"""
from datetime import datetime
from discord.ext import commands
from discord import Embed
from cogs.reaction_roles import ReactionRoles
from cogs.rules_verify import RulesVerify


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

    @commands.command(name="refresh-all", help="Refreshes both reactions and rules")
    @commands.has_role("Moderator")
    async def refresh_all(self, ctx: commands.Context):
        """refresh_all
        refreshs both the rules and reaction message
        Parameters
        ----------
            ctx {discord.ext.commands.Context} -- Context of the command.

        """
        await RulesVerify.refresh_message(self, ctx=ctx, delete=False)
        await ReactionRoles.refresh_reaction_message(self, ctx=ctx, delete=False)

    @commands.command(name="uptime", help="Gets uptime of bot")
    async def uptime(self, ctx: commands.Context):
        """uptime
        ---
        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        uptime = datetime.utcnow() - self.bot.uptime
        uptime_msg = ":clock1: Days: {}, Hours: {}, Minutes: {}, Seconds: {}".format(
            uptime.days,
            uptime.seconds // 3600,  # Hours
            (uptime.seconds // 60) % 60,  # Minutes
            uptime.seconds % 60,  # Seconds
        )

        start_time = self.bot.uptime.strftime("%Y-%m-%d %H:%M")
        description = "Bot has been online since {} UTC".format(start_time)
        await ctx.send(
            embed=Embed(title=uptime_msg, timestamp=ctx.message.created_at, description=description)
        )


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(Admin(bot))

"""Cogs for admin features"""
from datetime import datetime
from discord.ext import commands
from discord import Embed, PermissionOverwrite
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
        """Refresh_all
        refreshes both the rules and reaction message
        Parameters
        ----------
            ctx {discord.ext.commands.Context} -- Context of the command.

        """
        await RulesVerify.refresh_message(self, ctx=ctx, delete=False)
        await ReactionRoles.refresh_reaction_message(self, ctx=ctx, delete=False)

    @commands.command(name="uptime", help="Gets uptime of bot")
    async def uptime(self, ctx: commands.Context):
        """Uptime
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

    @commands.command(name="create-club", help="Create a new club")
    @commands.has_role("Moderator")
    async def create_club(self, ctx: commands.Context, name: str):
        """
        Creates a new club from the name provided

        :param name: Name of the club to make
        :param ctx: Context of the command.
        :type ctx: {discord.ext.commands.Context}
        :return:
        """
        await ctx.send(f"Creating roles for new club {name}")
        new_leadership = await self.bot.guild.create_role(
            name=f"{name.upper()} Leadership", hoist=True, mentionable=True
        )
        await self.bot.guild.create_role(name=f"{name}-general")
        student_role = await self.bot.get_role_from_name("student")
        professor_role = await self.bot.get_role_from_name("professor")
        alumni_role = await self.bot.get_role_from_name("alumni")
        await ctx.send(f"Creating channels for new club {name}")
        category = await self.bot.guild.create_category(
            name=name,
            overwrites={
                self.bot.guild.default_role: PermissionOverwrite(read_messages=False),
                student_role: PermissionOverwrite(read_messages=True, send_messages=True),
                professor_role: PermissionOverwrite(read_messages=True, send_messages=True),
                alumni_role: PermissionOverwrite(read_messages=True, send_messages=True),
                new_leadership: PermissionOverwrite(read_messages=True, send_messages=True),
            },
        )
        await self.bot.guild.create_text_channel(
            name=f"{name}-leadership",
            category=category,
            overwrites={
                self.bot.guild.default_role: PermissionOverwrite(read_messages=False),
                student_role: PermissionOverwrite(read_messages=False),
                professor_role: PermissionOverwrite(read_messages=False),
                alumni_role: PermissionOverwrite(read_messages=False),
                new_leadership: PermissionOverwrite(read_messages=True, send_messages=True),
            },
        )
        await self.bot.guild.create_text_channel(
            name=f"{name}-announcements",
            category=category,
            overwrites={
                self.bot.guild.default_role: PermissionOverwrite(read_messages=False),
                student_role: PermissionOverwrite(send_messages=False),
                professor_role: PermissionOverwrite(send_messages=False),
                alumni_role: PermissionOverwrite(send_messages=False),
                new_leadership: PermissionOverwrite(read_messages=True, send_messages=True),
            },
        )
        await self.bot.guild.create_text_channel(
            name=f"{name}-general",
            category=category,
            overwrites={
                self.bot.guild.default_role: PermissionOverwrite(read_messages=False),
            },
        )
        await ctx.send(
            "All roles and channels have been created.\n"
            "Still to do:\n"
            "  - Change color of new leadership role\n"
            "  - Update the reaction roles to include the new club"
        )


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(Admin(bot))

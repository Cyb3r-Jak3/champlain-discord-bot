"""Cog for dealing with graduations time"""
import cyberjake
import discord
from discord.ext import commands
from discord.utils import get
from discord import RawReactionActionEvent


class GraduationCog(commands.Cog, name="Graduation"):
    """Cog that deals with graduation message"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="set-graduation")
    @commands.has_role("Moderator")
    async def graduation_message(self, ctx: commands.Context, *, message_id):
        """Gets a message based of given message ID"""
        try:
            msg = await ctx.fetch_message(message_id)
        except discord.errors.NotFound:
            await cyberjake.error_embed(
                ctx, message="Message not found." "\nHint: Make sure same channel"
            )
            return
        if not msg:
            return
        await msg.add_reaction("🥳")
        await self.bot.update_last_message("last_graduation", msg.id)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        """On reaction the a user has their student role removed and Alumni role added"""
        user = self.bot.guild.get_member(payload.user_id)

        if payload.message_id != self.bot.latest_message_ids["last_graduation"] or user.bot:
            return
        student_role = get(self.bot.guild.roles, name="Student")
        if str(payload.emoji) != "🥳" or student_role not in user.roles:
            return
        alum_role = get(self.bot.guild.roles, name="Alumni")
        await user.remove_roles(student_role, reason="Graduation!")
        await user.add_roles(alum_role, reason="Graduation!")


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(GraduationCog(bot))

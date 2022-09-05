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
    async def graduation_message(self, ctx: commands.Context, *, message_id: int):
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
        """On reaction the user has their student role removed and Alumni role added"""
        guild: discord.Guild = self.bot.get_guild(payload.guild_id)
        member: discord.Member = guild.get_member(payload.user_id)
        if payload.message_id != self.bot.latest_message_ids["last_graduation"] or member.bot:
            return
        student_role = get(guild.roles, id=self.bot.guild_info[guild.id]["roles"]["student"])
        if str(payload.emoji) != "🥳" or student_role not in member.roles:
            return
        alum_role = get(guild.roles, id=self.bot.guild_info[guild.id]["roles"]["alumni"])
        await member.remove_roles(student_role, reason="Graduation!")
        await member.add_roles(alum_role, reason="Graduation!")


async def setup(bot):
    """Needed for extension loading"""
    await bot.add_cog(GraduationCog(bot))

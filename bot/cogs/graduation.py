"""Cog for dealing with graduations time"""

from typing import TYPE_CHECKING
import cyberjake
import discord
from discord.ext import commands
from discord.utils import get
from discord import RawReactionActionEvent, app_commands

if TYPE_CHECKING:
    from bot.bot import Discord_Bot


class GraduationCog(commands.Cog, name="Graduation"):
    """Cog that deals with graduation message"""

    def __init__(self, bot):
        self.bot: "Discord_Bot" = bot

    @app_commands.command(name="set-graduation", description="Sets the graduation message")
    @app_commands.checks.has_role("Moderator")
    async def graduation_message(self, interaction: discord.Interaction, message_id: str):
        """Gets a message based of given message ID"""
        try:
            msg = await interaction.channel.fetch_message(int(message_id))
        except discord.errors.NotFound:
            await cyberjake.error_embed(
                interaction, message="Message not found." "\nHint: Make sure same channel"
            )
            return
        if not msg:
            return
        await msg.add_reaction("🥳")
        await self.bot.update_last_message("last_graduation", msg.id)
        await interaction.response.send_message(
            f"Graduation message set to {msg.jump_url}", ephemeral=True
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        """On reaction the user has their student role removed and Alumni role added"""
        guild: discord.Guild = self.bot.get_guild(payload.guild_id)
        member: discord.Member = guild.get_member(payload.user_id)
        if payload.message_id != self.bot.latest_message_ids["last_graduation"] or member.bot:
            return
        student_role = get(guild.roles, id=self.bot.base_guild_info[guild.id]["roles"]["student"])
        if str(payload.emoji) != "🥳" or student_role not in member.roles:
            return
        alum_role = get(guild.roles, id=self.bot.base_guild_info[guild.id]["roles"]["alumni"])
        await member.remove_roles(student_role, reason="Graduation!")
        await member.add_roles(alum_role, reason="Graduation!")


async def setup(bot: commands.Bot) -> None:
    """Needed for extension loading"""
    await bot.add_cog(GraduationCog(bot))

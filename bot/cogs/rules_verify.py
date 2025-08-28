"""Cog for rule verification"""

from discord.ext import commands
from discord import app_commands
import discord
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from bot.bot import Discord_Bot


def load_files() -> Tuple[str, str]:
    """Loads the rules and getting started files"""
    with open("text/rules.txt", "r", encoding="utf-8") as f:
        rules = f.read()
    with open("text/getting_started.txt", "r", encoding="utf-8") as f:
        getting_started = f.read()
    return rules, getting_started


class RulesVerify(commands.Cog, name="Rules_Verify"):
    """Cogs for rules verifying"""

    def __init__(self, bot):
        self.bot: Discord_Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Sends user the rules when they join"""
        self.bot.log.debug("User: %s joined", member.name)
        accepted_rules_role = self.bot.load_role(member.guild.id, "role-request")
        rules, getting_started = load_files()
        await member.add_roles(accepted_rules_role, reason="User joined")
        await member.send(
            rules.format(
                mod_role="@Moderator",
                leader_role="@Leadership",
                homework_channel="#homework-help",
                troubleshooting_channel="#troubleshooting-questions",
            )
        )
        await member.send(
            getting_started.format(
                student_role="@Student",
                alumni_role="@Alumni",
                professor_role="@Professor",
            )
        )

    @app_commands.command(name="refresh-rules")
    @app_commands.checks.has_role("Moderator")
    async def refresh_message(self, interaction: discord.Interaction):
        """Refreshes the rules message"""
        await interaction.response.defer()
        rules_channel = self.bot.load_channel(interaction.guild.id, "rules-read-me")
        try:
            old_rules = await rules_channel.fetch_message(
                self.bot.latest_message_ids["last_rules"]
            )
            if old_rules is None:
                self.bot.log.warning("There is no old rules message")
            else:
                await old_rules.delete()
            old_started = await rules_channel.fetch_message(
                self.bot.latest_message_ids["last_started"]
            )
            if old_started is None:
                self.bot.log.warning("There is no old getting started message")
            else:
                await old_started.delete()
        except (
            commands.CommandInvokeError,
            AttributeError,
            discord.errors.HTTPException,
        ) as err:
            self.bot.log.error(err)

        guild_info = self.bot.guild_info[interaction.guild.id]
        rules, getting_started = load_files()
        new_message = await rules_channel.send(
            rules.format(
                mod_role=f"<@&{guild_info['roles']['moderator']}>",
                leader_role=f"<@&{guild_info['roles']['leadership']}>",
                homework_channel=f"<#{guild_info['channels']['homework-help']}>",
                troubleshooting_channel=f"<#{guild_info['channels']['troubleshooting-questions']}>",
            )
        )
        new_started = await rules_channel.send(
            getting_started.format(
                student_role=f"<@&{guild_info['roles']['student']}>",
                alumni_role=f"<@&{guild_info['roles']['alumni']}>",
                professor_role=f"<@&{guild_info['roles']['professor']}>",
            )
        )
        await new_message.pin(
            reason=f"Newest rules messages triggered by {interaction.user.display_name}"
        )
        await new_started.pin(
            reason=f"Newest getting started message triggered by {interaction.user.display_name}"
        )
        await self.bot.update_last_message("last_rules", new_message.id)
        await self.bot.update_last_message("last_started", new_started.id)


async def setup(bot: commands.Bot) -> None:
    """Needed for extension loading"""
    await bot.add_cog(RulesVerify(bot))

"""Cog for rule verification"""
import logging
import os
from discord.ext import commands
import discord


with open("text/rules.txt", "r") as f:
    rules = f.read()

with open("text/getting_started.txt", "r") as f:
    getting_started = f.read()

mod_role = os.environ["mod_role"]
leader_role = os.environ["leader_role"]
student_role = os.environ["student_role"]
alumni_role = os.environ["alumni_role"]
professor_role = os.environ["professor_role"]
homework = os.environ["homework_channel"]
troubleshooting = os.environ["troubleshooting_channel"]


class RulesVerify(commands.Cog, name="Rules_Verify"):
    """Cogs for rules verifying"""

    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("Champlain Discord")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Sends user the rules when they join"""
        self.log.debug("User: {} joined".format(member.name))
        await member.send(
            rules.format(
                mod_role="@Moderator",
                leader_role="@Leadership",
                homework_channel="#homework-help",
                troubleshooting_channel="#troubleshooting",
            )
        )
        await member.send(
            getting_started.format(
                student_role="@Student",
                alumni_role="@Alumni",
                professor_role="@Professor",
            )
        )

    @commands.command(name="accept", hidden=True)
    @commands.dm_only()
    async def accept_rules(self, ctx: commands.Context):
        """Assigns user the role-request role when they accept the rules"""
        self.log.info("User {} accepted the rules".format(ctx.author.name))
        member = self.bot.guild.get_member(ctx.message.author.id)
        accepted_rules_role = discord.utils.get(self.bot.guild.roles, name="role-request")
        await member.add_roles(accepted_rules_role, reason="Accepted the rules")
        embed = discord.Embed(
            title="Success",
            description="Thank you for accepting the rules. You'll now be able to request a role",
            timestamp=ctx.message.created_at,
        )
        await ctx.send(embed=embed)

    @commands.command(name="refresh-rules", hidden=True)
    @commands.has_role("Moderator")
    async def refresh_message(self, ctx: commands.Context, delete=True):
        """Refreshes the rules message"""
        if delete:
            await ctx.message.delete()
        try:
            old_rules = await self.bot.rules_channel.fetch_message(
                self.bot.latest_message_ids["last_rules"]
            )
            old_started = await self.bot.rules_channel.fetch_message(
                self.bot.latest_message_ids["last_started"]
            )
            await old_started.delete()
            await old_rules.delete()
        except (
            commands.CommandInvokeError,
            AttributeError,
            discord.errors.NotFound,
            discord.errors.HTTPException,
        ) as err:
            self.log.error(err)
        new_message = await self.bot.rules_channel.send(
            rules.format(
                mod_role=mod_role,
                leader_role=leader_role,
                homework_channel=homework,
                troubleshooting_channel=troubleshooting,
            )
        )
        new_started = await self.bot.rules_channel.send(
            getting_started.format(
                student_role=student_role,
                alumni_role=alumni_role,
                professor_role=professor_role,
            )
        )
        await new_message.pin(
            reason=f"Newest rules messages triggered by {ctx.author.display_name}"
        )
        await new_started.pin(
            reason=f"Newest getting started message triggered by {ctx.author.display_name}"
        )
        await self.bot.update_last_message("last_rules", new_message.id)
        await self.bot.update_last_message("last_started", new_started.id)


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(RulesVerify(bot))

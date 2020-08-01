"""Cog for rule verification"""
import logging
import os
from discord.ext import commands
import discord


with open("rules.txt", "r") as f:
    welcome_message = f.read()

mod_role = os.environ["mod_role"]
leader_role = os.environ["leader_role"]
student_role = os.environ["student_role"]
alumni_role = os.environ["alumni_role"]
professor_role = os.environ["professor"]


class RulesVerify(commands.Cog, name="Rules_Verify"):
    """Cogs for rules verifying"""

    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("Champlain Discord")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Sends user the rules when they join"""
        self.log.debug("User: {} joined".format(member.name))
        formatted_message = welcome_message.format(
            mod_role="@Moderator",
            leader_role="@Leadership",
            student_role="@Student",
            alumni_role="@Alumni",
            professor_role="@Professor",
        )
        formatted_message += "\n**Please response with `?accept` to get started.**"
        await member.send(formatted_message)

    @commands.command(name="accept", hidden=True)
    @commands.dm_only()
    async def accept_rules(self, ctx: commands.Context):
        """Assigns user the role-request role when they accept the rules"""
        self.log.info("User {} accepted the rules".format(ctx.author.name))
        member = self.bot.guild.get_member(ctx.message.author.id)
        accepted_rules_role = discord.utils.get(self.bot.guild.roles, name="role-request")
        await member.add_roles(accepted_rules_role)
        embed = discord.Embed(
            title="Success",
            description="Thank you for accepting the rules. You'll now be able to request a role",
            timestamp=ctx.message.created_at,
        )
        await ctx.send(embed=embed)

    @commands.command(name="refresh_rules", hidden=True)
    @commands.has_role("Moderator")
    async def refresh_message(self, ctx: commands.Context):
        """Refreshes the rules message"""
        await ctx.message.delete()
        try:
            old_message = await self.bot.rules_channel.fetch_message(
                self.bot.latest_message_ids["last_rules"]
            )
            await old_message.delete()
        except (
            commands.CommandInvokeError,
            AttributeError,
            discord.errors.NotFound,
            discord.errors.HTTPException,
        ) as err:
            self.log.error(err)
        new_message = await self.bot.rules_channel.send(
            welcome_message.format(
                mod_role=mod_role,
                leader_role=leader_role,
                student_role=student_role,
                alumni_role=alumni_role,
                professor_role=professor_role,
            )
        )
        await new_message.pin()
        await self.bot.update_last_message("last_rules", new_message.id)


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(RulesVerify(bot))

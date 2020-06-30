"""Cog for rule verification"""
import logging
from discord.ext import commands
import discord


welcome_message = open("rules.txt", "r").read()


class RulesVerify(commands.Cog, name="Rules_Verify"):
    """Cogs for rules verifying"""

    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("Champlain Discord")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Sends user the rules when they join"""
        self.log.debug("User: {} joined".format(member.name))
        embed = discord.Embed(
            title="Welcome:",
            description=welcome_message.format(mod_role="@Moderator", leader_role="@Leadership"),
            timestamp=member.joined_at,
        )
        await member.send(embed=embed)

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
    async def refresh_message(self, _):
        """Refreshes the rules message"""
        try:
            old_message = await self.bot.rules_channel.fetch_message(
                self.bot.latest_message_ids["last_rules"]
            )
            await old_message.delete()
        except (commands.CommandInvokeError, AttributeError, discord.errors.NotFound) as e:
            self.log.error(e)
        embed = discord.Embed(
            title="Welcome!",
            description=welcome_message[:-50].format(
                mod_role="<@&716775554757689367>", leader_role="<@&716775554757689368>"
            ),
        )
        new_message = await self.bot.rules_channel.send(embed=embed)
        await new_message.pin()
        await self.bot.update_last_message("last_rules", new_message.id)


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(RulesVerify(bot))

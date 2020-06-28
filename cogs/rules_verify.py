"""Cog for rule verification"""
import logging
from discord.ext import commands
import discord


welcome_message = """Welcome to the Official Discord for:
- **Association for Computing Machinery (ACM)**
- **Champlain Cyber Security Club (CCSC)**
- **Champlain College Digital Forensics Association (DFA)**
- **Women in Technology Club (WiT)**

This is a **student run discord**.
All people who have roles of leadership are current students and people with moderator role former student/ex-leadership.
While professors may be on here, they don’t control the discord and have limited access. While professors may be on here, they don’t control the discord and have limited access.Go to the #how-to-use channel to read how the server is set up and who has access to what.

The **main rules** for the server are below. This is a chilled out environment so we don't ask much:
*1) If you wouldn't say it in person to those on the other end, don't say it here.*
*2) Treat everyone with respect.*
*3) Don't be an asshole.*
If there is something that makes you uncomfortable please bring it to the attention of our {mod_role} or {leader_role} -- **there is nothing too big or too small.** We are still a part of the Champlain community. 

If {mod_role} or {leader_role} has an issue with your post or has gotten reports about your actions, there is a 3 strike policy:
**Strike 1** - Warning message and a probable removable of offensive content
**Strike 2** - 1 week suspension *(could be longer depending on the post and is at the discretion of {mod_role} & {leader_role})*
**Strike 3** - Banned from the server indefinitely

The focus of this discord is to create a computer focused community for Champlain students. Our fields overlap with many other fields including politics. Just remember to be courteous of others.

Please response with `?accept` to get started
"""


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

    @commands.command(name="refresh_message", hidden=True)
    async def refresh_message(self, _):
        """Refreshes the rules message"""
        embed = discord.Embed(
            title="Welcome!",
            description=welcome_message[:-50].format(
                mod_role="<@&716775554757689367>", leader_role="<@&716775554757689368>"
            ),
        )
        new_message = await self.bot.rules_channel.send(embed=embed)
        await new_message.pin()


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(RulesVerify(bot))

"""Cog for reaction roles"""
import logging
from discord.ext import commands
from discord.utils import get
from discord import RawReactionActionEvent, errors

reaction_role_message = """
**React to get club specific notifications**
:one: for ACM, :two: for CCSC, :three: for DFA, :four: for WiT :five: for NECCDC Interest"""


class ReactionRoles(commands.Cog, name="Reaction_Roles"):
    """Cogs for reaction roles"""

    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("Champlain Discord")

    @commands.command(name="refresh-reactions", hidden=True)
    @commands.has_role("Moderator")
    async def refresh_reaction_message(self, ctx: commands.Context, delete=True):
        """Command that generates a new role reaction message and updates it in redis cache"""
        if delete:
            await ctx.message.delete()
        try:
            old_message = await self.bot.rules_channel.fetch_message(
                self.bot.latest_message_ids["last_reaction"]
            )
            await old_message.delete()
        except (
            commands.CommandInvokeError,
            AttributeError,
            errors.NotFound,
            errors.HTTPException,
        ) as err:
            self.log.error(err)
        new_message = await self.bot.rules_channel.send(reaction_role_message)
        await new_message.pin()
        await self.bot.update_last_message("last_reaction", new_message.id)
        for reaction in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]:
            await new_message.add_reaction(reaction)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        """
        Adds a new role on reaction
        Parameters
        ----------
        payload Discord.Payload of the raw event

        """
        user = self.bot.guild.get_member(payload.user_id)
        if payload.message_id != self.bot.latest_message_ids["last_reaction"] or user.bot:
            return
        emoji = str(payload.emoji)
        if emoji == "1️⃣":
            self.log.debug("Adding ACM to {}".format(user.name))
            role = get(self.bot.guild.roles, name="acm-general")
        elif emoji == "2️⃣":
            self.log.debug("Adding CCSC to {}".format(user.name))
            role = get(self.bot.guild.roles, name="ccsc-general")
        elif emoji == "3️⃣":
            self.log.debug("Adding DFA to {}".format(user.name))
            role = get(self.bot.guild.roles, name="dfa-general")
        elif emoji == "4️⃣":
            self.log.debug("Adding WIT to {}".format(user.name))
            role = get(self.bot.guild.roles, name="wit-general")
        elif emoji == "5️⃣":
            self.log.debug("Adding NECCDC to {}".format(user.name))
            role = get(self.bot.guild.roles, name="neccdc-interest")
        else:
            return
        await user.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        """
        Removed a role on removal of reaction
        Parameters
        ----------
        payload Discord.Payload of the raw event
        """
        user = self.bot.guild.get_member(payload.user_id)
        if payload.message_id != self.bot.latest_message_ids["last_reaction"] or user.bot:
            return
        emoji = str(payload.emoji)
        if emoji == "1️⃣":
            self.log.debug("Removing ACM from {}".format(user.name))
            role = get(self.bot.guild.roles, name="acm-general")
        elif emoji == "2️⃣":
            self.log.debug("Removing CCSC from {}".format(user.name))
            role = get(self.bot.guild.roles, name="ccsc-general")
        elif emoji == "3️⃣":
            self.log.debug("Removing DFA from {}".format(user.name))
            role = get(self.bot.guild.roles, name="dfa-general")
        elif emoji == "4️⃣":
            self.log.debug("Removing WIT from {}".format(user.name))
            role = get(self.bot.guild.roles, name="wit-general")
        elif emoji == "5️⃣":
            self.log.debug("Removing NECCDC to {}".format(user.name))
            role = get(self.bot.guild.roles, name="neccdc-interest")
        else:
            return
        await user.remove_roles(role)


def setup(bot):
    """Needed for extension loading"""
    bot.add_cog(ReactionRoles(bot))

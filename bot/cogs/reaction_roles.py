"""Cog for reaction roles"""
from discord.ext import commands
from discord.utils import get
from discord import RawReactionActionEvent, errors


class ReactionRoles(commands.Cog, name="Reaction_Roles"):
    """Cogs for reaction roles"""

    def __init__(self, bot):
        self.bot = bot

    async def role_action(self, payload: RawReactionActionEvent, action: str) -> None:
        """Performs a role action (add or remove) on a user"""
        user = self.bot.guild.get_member(payload.user_id)
        if payload.message_id != self.bot.latest_message_ids["last_reaction"] or user.bot:
            return
        match str(payload.emoji):
            case "1️⃣":
                role = get(self.bot.guild.roles, name="acm-general")
            case "2️⃣":
                role = get(self.bot.guild.roles, name="ccsc-general")
            case "3️⃣":
                role = get(self.bot.guild.roles, name="dfa-general")
            case "4️⃣":
                role = get(self.bot.guild.roles, name="wit-general")
            case "5️⃣":
                role = get(self.bot.guild.roles, name="neccdc-interest")
            case "6️⃣":
                role = get(self.bot.guild.roles, name="math-club-general")
            case _:
                return
        if action == "add":
            self.bot.log.debug("Adding {} to {}".format(role.name, user.name))
            await user.add_roles(role, reason="Reaction Roles")
        elif action == "remove":
            self.bot.log.debug("Removing {} from {}".format(role.name, user.name))
            await user.remove_roles(role, reason="Reaction Roles")
        else:
            raise NotImplementedError
        return

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
            if old_message is None:
                self.bot.log.warning("There is no old reactions message")
                return
            await old_message.delete()
        except (
            commands.CommandInvokeError,
            AttributeError,
            errors.NotFound,
            errors.HTTPException,
        ) as err:
            self.bot.log.error(err)
        with open("text/reaction_roles.txt", encoding="utf-8") as infile:
            new_message = await self.bot.rules_channel.send(infile.read())
        await new_message.pin(
            reason=f"Newest reaction role message triggered by {ctx.author.display_name}"
        )
        await self.bot.update_last_message("last_reaction", new_message.id)
        for reaction in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]:
            await new_message.add_reaction(reaction)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        """
        Adds a new role on reaction
        Parameters
        ----------
        payload Discord.Payload of the raw event

        """
        return await self.role_action(payload, "add")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        """
        Removed a role on removal of reaction
        Parameters
        ----------
        payload Discord.Payload of the raw event
        """
        return await self.role_action(payload, "remove")


async def setup(bot):
    """Needed for extension loading"""
    await bot.add_cog(ReactionRoles(bot))

"""Cog for reaction roles"""

import discord
from discord.ext import commands
from discord.utils import get
from discord import RawReactionActionEvent, errors, app_commands


class ReactionRoles(commands.Cog, name="Reaction_Roles"):
    """Cogs for reaction roles"""

    def __init__(self, bot):
        self.bot = bot

    async def role_action(self, payload: RawReactionActionEvent, action: str) -> None:
        """Performs a role action (add or remove) on a user"""
        guild: discord.Guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)
        if payload.message_id != self.bot.latest_message_ids["last_reaction"] or user.bot:
            return
        match str(payload.emoji):
            case "1️⃣":
                role = get(guild.roles, name="acm-general")
            case "2️⃣":
                role = get(guild.roles, name="ccsc-general")
            case "3️⃣":
                role = get(guild.roles, name="dfa-general")
            case "4️⃣":
                role = get(guild.roles, name="wit-general")
            case "5️⃣":
                role = get(guild.roles, name="neccdc-interest")
            case "6️⃣":
                role = get(guild.roles, name="math-club-general")
            case "7️⃣":
                role = get(guild.roles, name="doc-general")
            case _:
                return
        if action == "add":
            self.bot.log.debug("Adding %s to %s", role.name, user.name)
            await user.add_roles(role, reason="Reaction Roles")
        elif action == "remove":
            self.bot.log.debug("Removing %s from %s", role.name, user.name)
            await user.remove_roles(role, reason="Reaction Roles")
        else:
            raise NotImplementedError
        return

    @app_commands.command(name="refresh-reactions")
    @app_commands.checks.has_role("Moderator")
    async def refresh_reaction_message(self, interaction: discord.Interaction):
        """Command that generates a new role reaction message and updates it in redis cache"""
        rules_channel = self.bot.load_channel(interaction.guild.id, "rules-read-me")
        try:
            if self.bot.latest_message_ids["last_reaction"] is not None:
                old_message = await rules_channel.fetch_message(
                    self.bot.latest_message_ids["last_reaction"]
                )
                if old_message is None:
                    self.bot.log.warning("There is no old reactions message")
                else:
                    await old_message.delete()
            else:
                self.bot.log.warning("There is no old reactions message ID")
        except (
            commands.CommandInvokeError,
            AttributeError,
            errors.NotFound,
        ) as err:
            self.bot.log.error(err)
        with open("text/reaction_roles.txt", encoding="utf-8") as infile:
            new_message = await rules_channel.send(infile.read())
        await new_message.pin(
            reason=f"Newest reaction role message triggered by {interaction.user.display_name}"
        )
        await self.bot.update_last_message("last_reaction", new_message.id)
        for reaction in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]:
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


async def setup(bot: commands.Bot) -> None:
    """Needed for extension loading"""
    await bot.add_cog(ReactionRoles(bot))

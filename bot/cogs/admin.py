"""Cogs for admin features"""
from datetime import datetime
from typing import List
import discord
from discord.ext import commands
from discord import Embed, PermissionOverwrite, app_commands
from .reaction_roles import ReactionRoles
from .rules_verify import RulesVerify


class Admin(commands.Cog, name="Admin"):
    """Cogs for admin commands"""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reload-extension", description="reloads <extension>")
    @app_commands.checks.has_role("Moderator")
    async def reload_extension(self, interaction: discord.Interaction, extension: str):
        """reload_extension
        ---

        Command that reloads an extension.

        Arguments:
            ctx {discord.ext.commands.Context} -- Context of the command.
            extension {str} -- extension to reload
        """
        await self.bot.reload_extension(extension)
        await interaction.response.send_message(f"Extension {extension} reloaded", ephemeral=True)

    @app_commands.command(name="refresh-all", description="Refreshes both reactions and rules")
    @app_commands.checks.has_role("Moderator")
    async def refresh_all(self, interaction: discord.Interaction):
        """Refresh_all
        refreshes both the rules and reaction message
        Parameters
        ----------
            ctx {discord.ext.commands.Context} -- Context of the command.

        """
        await RulesVerify.refresh_message(self, interaction=interaction)
        await ReactionRoles.refresh_reaction_message(self, interaction=interaction)

    @app_commands.command(name="uptime", description="Gets uptime of bot")
    async def uptime(self, interaction: discord.Interaction):
        """Uptime
        ---
        Arguments:
        ---
            ctx {discord.ext.commands.Context} -- Context of the command.
        """
        uptime = datetime.utcnow() - self.bot.uptime
        uptime_msg = (
            ":clock1: Days: {}, Hours: {}, Minutes: {}, Seconds: {}".format(  # pylint: disable=C0209
                uptime.days,
                uptime.seconds // 3600,  # Hours
                (uptime.seconds // 60) % 60,  # Minutes
                uptime.seconds % 60,  # Seconds
            )
        )

        start_time = self.bot.uptime.strftime("%Y-%m-%d %H:%M")
        description = f"Bot has been online since {start_time} UTC"
        await interaction.response.send_message(
            embed=Embed(title=uptime_msg, timestamp=interaction.created_at, description=description),
            ephemeral=True,
        )

    @app_commands.command(name="set-message", description="Manually set a message key")
    @app_commands.checks.has_role("Moderator")
    async def manual_message_set(self, interaction: discord.Interaction, key: str, value: str):
        if key not in self.bot.latest_message_ids.keys():
            return await interaction.response.send_message(f"Key {key} is not valid", ephemeral=True)
        await self.bot.update_last_message(key, value)
        await interaction.response.send_message(
            f"Key: `{key}` has been set to **{value}**", ephemeral=True
        )

    @app_commands.command(name="get-message", description="Get a message key")
    @app_commands.checks.has_role("Moderator")
    async def manual_message_get(self, interaction: discord.Interaction, message_key: str):
        if message_key not in list(self.bot.latest_message_ids.keys()) + ["all"]:
            return await interaction.response.send_message(
                f"Key {message_key} is not valid", ephemeral=True
            )
        if message_key == "all":
            embed = discord.Embed(title="All message keys", color=discord.Color.blue())
            for key, value in self.bot.latest_message_ids.items():
                embed.add_field(name=key, value=value, inline=False)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        value = await self.bot.get_last_message(message_key)
        await interaction.response.send_message(f"Key: `{message_key}`: **{value}**", ephemeral=True)

    @manual_message_get.autocomplete("message_key")
    async def manual_message_set_autocomplete(
        self, _: discord.Interaction, current: str
    ) -> List[app_commands.Choice[str]]:
        return [
            app_commands.Choice(name=key, value=key)
            for key in list(self.bot.latest_message_ids.keys()) + ["all"]
            if current.lower() in key.lower()
        ]

    @app_commands.command(name="create-club", description="Create a new club")
    @app_commands.checks.has_permissions(administrator=True)
    async def create_club(self, interaction: discord.Interaction, name: str):
        """
        Creates a new club from the name provided

        :param interaction:
        :param name: Name of the club to make
        :return:
        """
        await interaction.response.send_message(
            f"Creating roles for new club {name}", ephemeral=True
        )
        guild = interaction.guild
        new_leadership = await guild.create_role(
            name=f"{name.upper()} Leadership", hoist=True, mentionable=True
        )
        await guild.create_role(name=f"{name}-general")
        student_role = self.bot.load_role(guild.id, "student")
        professor_role = self.bot.load_role(guild.id, "professor")
        alumni_role = self.bot.load_role(guild.id, "alumni")
        await interaction.followup.send_message(f"Creating channels for new club {name}")
        category = await guild.create_category(
            name=name,
            overwrites={
                guild.default_role: PermissionOverwrite(read_messages=False),
                student_role: PermissionOverwrite(read_messages=True, send_messages=True),
                professor_role: PermissionOverwrite(read_messages=True, send_messages=True),
                alumni_role: PermissionOverwrite(read_messages=True, send_messages=True),
                new_leadership: PermissionOverwrite(read_messages=True, send_messages=True),
            },
        )
        await guild.create_text_channel(
            name=f"{name}-leadership",
            category=category,
            overwrites={
                guild.default_role: PermissionOverwrite(read_messages=False),
                student_role: PermissionOverwrite(read_messages=False),
                professor_role: PermissionOverwrite(read_messages=False),
                alumni_role: PermissionOverwrite(read_messages=False),
                new_leadership: PermissionOverwrite(read_messages=True, send_messages=True),
            },
        )
        await guild.create_text_channel(
            name=f"{name}-announcements",
            category=category,
            overwrites={
                guild.default_role: PermissionOverwrite(read_messages=False),
                student_role: PermissionOverwrite(send_messages=False),
                professor_role: PermissionOverwrite(send_messages=False),
                alumni_role: PermissionOverwrite(send_messages=False),
                new_leadership: PermissionOverwrite(read_messages=True, send_messages=True),
            },
        )
        await guild.create_text_channel(
            name=f"{name}-general",
            category=category,
            overwrites={
                guild.default_role: PermissionOverwrite(read_messages=False),
            },
        )
        await interaction.edit_original_response(
            content="All roles and channels have been created.\n"
            "Still to do:\n"
            "  - Change color of new leadership role\n"
            "  - Update the reaction roles to include the new club"
        )


async def setup(bot):
    """Needed for extension loading"""
    await bot.add_cog(Admin(bot))

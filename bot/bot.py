"""Main Bot File"""

import json
import os
from datetime import datetime
from typing import Optional
import sys

import discord
from discord.ext import commands
from log_maker import make_logger

TOKEN = os.environ["DISCORD_TOKEN"]
log = make_logger("Champlain Discord", os.getenv("LOG_LEVEL", "INFO"))
data_directory = os.getenv("DATA_DIR", "/data")

initial_extensions = ["cogs.rules_verify", "cogs.reaction_roles", "cogs.admin", "cogs.graduation"]
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
description = (
    "Champlain Discord bot. Does rule verification and reaction roles.\n"
    "Source: https://github.com/Cyb3r-Jak3/champlain-discord-bot"
)
with open("./text/info.json", encoding="utf-8") as f:
    base_guild_info = json.load(f)

log.debug(
    "Using discord.py version: %s and Python version %s",
    discord.__version__,
    sys.version[0:5],
)


def total_ids() -> dict:
    """Gets all the ids"""
    return {
        "last_reaction": _get_message_id("last_reaction"),
        "last_rules": _get_message_id("last_rules"),
        "last_started": _get_message_id("last_started"),
        "last_graduation": _get_message_id("last_graduation"),
    }


def _set_last_message_id(key: str, message: int) -> None:
    """
    Sets the message ID in redis cache
    Parameters
    ----------
    message The message id of the key

    """
    if key not in total_ids():
        return None
    with open(f"{data_directory}/{key}", "w+", encoding="utf-8") as outfile:
        outfile.write(str(message))


def _get_message_id(key: str) -> Optional[int]:
    """
    Returns the role reaction message from redis cache
    Returns
    -------
    int - ID of the last role_reaction_message
    """
    if key not in ["last_reaction", "last_rules", "last_started", "last_graduation"]:
        return
    try:
        with open(f"{data_directory}/{key}", "r", encoding="utf-8") as infile:
            return int(infile.read())
    except (AttributeError, FileNotFoundError) as err:
        log.error("Error getting key '%s': %s", key, err)


class Discord_Bot(commands.Bot):  # pylint: disable=missing-class-docstring
    def __init__(self):
        super().__init__(
            command_prefix="?", intents=intents, description=description, help_command=None
        )
        self.uptime = datetime.utcnow()
        self.latest_message_ids = total_ids()
        self.log = log
        self.guild_info: dict = {}
        self.bot_roles: dict[int, discord.Role] = {}

    def load_guild_info(self, guild: discord.Guild):
        """Loads the guild info from the base_guild_info file
        and updates it with the guild's info."""
        new_copy = base_guild_info.copy()
        self.bot_roles[guild.id] = discord.utils.get(guild.roles, name=self.user.name)
        for role in new_copy["roles"].keys():
            try:
                new_copy["roles"][role] = discord.utils.find(
                    lambda r: r.name.lower() == role, guild.roles  # skipcq: PYL-W0640
                ).id
            except AttributeError as err:
                log.error("Error loading role '%s' for guild %s: %s", role, guild.name, err)
        for channel in new_copy["channels"]:
            try:
                new_copy["channels"][channel] = discord.utils.find(
                    lambda c: c.name.lower() == channel, guild.channels  # skipcq: PYL-W0640
                ).id
            except AttributeError as err:
                log.error("Error loading channel '%s' for guild %s: %s", channel, guild.name, err)
        self.guild_info[guild.id] = new_copy

    def load_channel(self, guild: int, name: str) -> discord.TextChannel:
        """Loads the channel from the guild info"""
        return self.get_channel(self.guild_info[guild]["channels"][name])

    def load_role(self, guild: int, name: str) -> discord.Role:
        """Loads the role from the guild info"""
        return self.get_guild(guild).get_role(self.guild_info[guild]["roles"][name])

    async def on_ready(self):
        """When bot has connected to Discord"""
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                self.log.info("Loaded extension %s", extension)
            except commands.ExtensionError as e:
                self.log.error("Failed to load extension %s. %s", extension, e)
        self.log.info("Logged in as %s", self.user)
        for guild in self.guilds:
            self.log.info("Loading guild info for %s", guild.name)
            self.load_guild_info(guild)
        await self.change_presence(
            activity=discord.Activity(name="/uptime", type=discord.ActivityType.playing)
        )
        await self.tree.sync()
        self.log.info("Online")

    async def update_last_message(self, key: str, message_id: int):
        """
        Updates the last message id both in redis cache and for the bot.
        Parameters
        ----------
        message_id The ID of the latest reaction message

        """
        self.latest_message_ids[key] = message_id
        _set_last_message_id(key, message_id)

    async def get_last_message(self, key: str):
        """
        Gets the last message id both for the bot.
        Parameters
        ----------
        message_id The ID of the latest reaction message

        """
        return self.latest_message_ids[key]


bot = Discord_Bot()
bot.run(TOKEN, reconnect=True)

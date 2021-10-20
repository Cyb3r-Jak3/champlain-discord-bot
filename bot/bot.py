"""Main Bot File"""
import os
import re
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse
import discord
from discord.ext import commands
import redis
from cyberjake import make_logger

TOKEN = os.environ["DISCORD_TOKEN"]
OWNER_NAME = os.environ["OWNER_NAME"]
guild_id = int(os.environ["GUILD_ID"])
channel_id = int(os.environ["CHANNEL_ID"])
log_level = os.getenv("LOG_LEVEL", "INFO")

log = make_logger("Champlain Discord", log_level)
url = urlparse(os.environ.get("REDIS_URL"))
r = redis.Redis(
    host=url.hostname,
    port=url.port,
    username=url.username,
    password=url.password,
    ssl=False,
    ssl_cert_reqs=None,
)
initial_extensions = ["cogs.rules_verify", "cogs.reaction_roles", "cogs.admin", "cogs.graduation"]
intents = discord.Intents.default()
intents.members = True  # pylint: disable=E0237
description = (
    "Champlain Discord bot. Does rule verification and reaction roles.\n"
    "Source: https://github.com/Cyb3r-Jak3/champlain-discord-bot"
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
    r.set(key, message)


def _get_message_id(key: str) -> int:
    """
    Returns the role reaction message from redis cache
    Returns
    -------
    int - ID of the last role_reaction_message
    """
    try:
        return int(r.get(key).decode("utf-8"))
    except AttributeError:
        pass


class Discord_Bot(commands.Bot):  # pylint: disable=missing-class-docstring
    def __init__(self):
        super().__init__(command_prefix="?", intents=intents)
        self.uptime = datetime.utcnow()
        self.latest_message_ids = total_ids()
        self.guild, self.rules_channel = "", ""
        self.description = description

    async def on_ready(self):
        """When bot has connected to Discord"""
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except commands.ExtensionError as e:
                log.error("Failed to load extension {}. {}".format(extension, e))
        self.guild = self.get_guild(guild_id)
        self.rules_channel = self.get_channel(channel_id)
        await self.change_presence(
            activity=discord.Activity(name="?help", type=discord.ActivityType.playing)
        )
        log.info("Online")

    async def get_role_from_name(self, role_name: str) -> Optional[discord.Role]:
        """
        Pulls role from Environment variables
        :param role_name: The name of the role to get from the environment
        :return:
        """
        if not role_name.endswith("_role"):
            role_name += "_role"
        role = os.environ.get(role_name)
        if not role:
            return
        return self.guild.get_role(int(re.search(r"\d+", role).group()))

    async def update_last_message(self, key: str, message_id: int):
        """
        Updates the last message id both in redis cache and for the bot.
        Parameters
        ----------
        message_id The ID of the latest reaction message

        """
        self.latest_message_ids[key] = message_id
        _set_last_message_id(key, message_id)


bot = Discord_Bot()
bot.run(TOKEN, reconnect=True)

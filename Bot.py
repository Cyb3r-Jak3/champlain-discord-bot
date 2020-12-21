"""Main Bot File"""
import os
from datetime import datetime
import discord
from discord.ext import commands
import redis
import log_maker

TOKEN = os.environ["DISCORD_TOKEN"]
OWNER_NAME = os.environ["OWNER_NAME"]
OWNER_ID = os.environ["OWNER_ID"]
guild_id = int(os.environ["GUILD_ID"])
channel_id = int(os.environ["CHANNEL_ID"])
log_level = os.getenv("LOG_LEVEL", "INFO")

log = log_maker.make_logger("Champlain Discord", log_level)
r = redis.from_url(os.environ["REDIS_URL"])
initial_extensions = ["cogs.rules_verify", "cogs.reaction_roles", "cogs.admin", "cogs.graduation"]
intents = discord.Intents.default()
intents.members = True
description = (
    "Champlain Discord bot. Does rule verification and reaction roles.\n"
    "Source: https://gitlab.com/Cyb3r-Jak3/champlain_discord_bot"
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
        super().__init__(command_prefix="?", owner_id=OWNER_ID, intents=intents)
        self.uptime = datetime.utcnow()
        self.latest_message_ids = total_ids()
        self.guild, self.rules_channel = "", ""
        self.description = description

    async def on_ready(self):
        """When bot has connected to Discord"""
        log.info("Online")
        self.guild = self.get_guild(guild_id)
        self.rules_channel = self.get_channel(channel_id)
        await self.change_presence(
            activity=discord.Activity(name="?help", type=discord.ActivityType.playing)
        )
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except commands.ExtensionError as e:
                log.error("Failed to load extension {}. {}".format(extension, e))

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

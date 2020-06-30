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
redis_url = os.environ["REDIS_URL"]
guild_id = int(os.environ["GUILD_ID"])
channel_id = int(os.environ["CHANNEL_ID"])
log_level = os.getenv("LOG_LEVEL")
if not log_level:
    log_level = "INFO"


log = log_maker.make_logger("Champlain Discord", log_level)
r = redis.from_url(redis_url)
initial_extensions = ["cogs.rules_verify", "cogs.reaction_roles", "cogs.admin"]


def total_ids() -> dict:
    """Gets all the ids"""
    return {
        "last_reaction": get_message_id("last_reaction"),
        "last_rules": get_message_id("last_rules"),
    }


def set_last_message_id(key: str, message: int) -> None:
    """
    Sets the message ID in redis cache
    Parameters
    ----------
    message The message id of the key

    """
    r.set(key, message)


def get_message_id(key: str) -> int:
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
        super().__init__(command_prefix="?", owner_id=OWNER_ID)
        self.uptime = datetime.utcnow()
        self.latest_message_ids = total_ids()
        self.guild, self.rules_channel = "", ""

    async def on_ready(self):
        """
        When bot has connected to discord
        """
        log.info("Online")
        self.guild = self.get_guild(guild_id)
        self.rules_channel = self.get_channel(channel_id)
        log.debug(self.guild.name)
        log.debug(self.rules_channel.name)
        log.debug(self.latest_message_ids)
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
        set_last_message_id(key, message_id)


bot = Discord_Bot()
bot.run(TOKEN, reconnect=True)

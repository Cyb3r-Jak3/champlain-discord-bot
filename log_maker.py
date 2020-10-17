"""Makes the logger for the program"""
import logging


def make_logger(name: str, log_level: str) -> logging.Logger:
    """Make_logger
    ---

    Creates the logger that is used by the bot. Also imported to cogs and datahandler.

    Arguments:
    ---
        name {str} -- Name of the logger
        log_level {str} -- The logging level. Valid strings are
            'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'

    Returns:
    ---
        logging.Logger -- Logger class that handled the logging.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(
        "%(levelname)s - %(name)s - %(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

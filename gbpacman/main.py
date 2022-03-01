from os import path as os_path
from plogger import get_logger

from gbpacman.utils.cmdline import get_cmd_options

logger = get_logger(os_path.basename(__file__))
logger.debug("Hello")


def main():
    logger.info("Inside main")
    get_cmd_options()

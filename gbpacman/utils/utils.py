import json
from plogger import get_logger

logger = get_logger(__name__)


def load_settings(json_filepath):
    try:
        with open(json_filepath) as file:
            return json.load(file)
    except FileNotFoundError as error:
        logger.error(error)
        return {}


def print_attributes(obj):
    for key, value in vars(obj).items():
        logger.info("%s : %s" % (key, value))

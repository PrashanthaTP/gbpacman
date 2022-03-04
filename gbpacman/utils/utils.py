import json
from plogger import get_logger

logger = get_logger(__file__.split(".")[0])


def load_settings(json_filepath):
    try:
        with open(json_filepath) as file:
            return json.load(file)
    except FileNotFoundError as error:
        logger.error(error)
        return {}

from os import path as os_path
from plogger import get_logger

from gbpacman.utils import get_cmd_options
from gbpacman.utils import load_settings

logger = get_logger(os_path.basename(__file__))
logger.debug("Hello")

ROOT_DIR=os_path.dirname(os_path.abspath(__file__))
SETTINGS_FILE="settings.json"




def main():
    get_cmd_options()
    settings = load_settings(os_path.join(ROOT_DIR,SETTINGS_FILE))
    print(settings)

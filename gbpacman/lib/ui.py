from gbpacman.utils import get_global_logger

logger = get_global_logger()


def display_packages(packages: list):
    if len(packages) == 0:
        logger.warning("No pakcages to display")
    for package in packages:
        print("-"*30)
        print(f"Name    : {package.name}")
        print(f"Version : {package.version}")
        print(f"About   : {package.description}")
    print("-"*30)

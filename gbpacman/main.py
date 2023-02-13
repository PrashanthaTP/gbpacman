from os import path as os_path

from gbpacman.utils import (get_cmd_options,
                            load_settings,
                            get_global_logger)

from gbpacman.lib import (calls,
                          parser,
                          filters,
                          api,
                          ui)
from gbpacman.config import settings

logger = get_global_logger()

SETTINGS_FILE = "settings.json"
BIN_DIR = os_path.join(settings["BASE_DIR"], "bin")
MSYS_URL = settings["packages_url"]


def get_response(query):
    url = f"{MSYS_URL}/search?q={query}"
    logger.debug(f"Pinging...{url}")
    response = calls.ping_url(url)
    return response


def get_list_of_packages(package_name):
    response = get_response(query=package_name)
    calls.check_response(response)
    target_tag = parser.extract(response,
                                filters.is_search_table,
                                attrs={"class": "card mb-3"},
                                limit=1)[0]
    _, table = parser.get_package_table(target_tag)
    packages_list = parser.get_packages_list(table)
    return packages_list


def list_matching_packages(package_name):
    packages = get_list_of_packages(package_name)
    ui.display_packages(packages)


# TODO:
# Rethink about selecting first package from
# packages_list
def install_package(package_name):
    # installs the first package found when searched
    packages_list = get_list_of_packages(package_name)
    if len(packages_list) == 0:
        logger.error("No package found matching the name: %s" % (package_name))
        return

    downloaded_file = api.download_package(packages_list[0])
    if downloaded_file is not None:  # if not already installed
        api.install_downloaded_package(downloaded_file, packages_list[0].name)
    logger.info("Please add '%s' to path" %
                (os_path.join(settings["installation_dir"], "usr", "bin")))


def install_from_url(url:str):
    package = parser.make_package(url)
    downloaded_file = api.download_package_from_url(package)

    if downloaded_file is not None:  # if not already installed
        api.install_downloaded_package(downloaded_file, package.name)
    logger.info("Please add '%s' to path" %
                (os_path.join(settings["installation_dir"], "usr", "bin")))

def main():
    options = get_cmd_options(settings)
    if options.list:
        list_matching_packages(package_name)
    if options.install:
        install_package(package_name)
    if options.install_from_url:
        install_from_url(url=options.install_from_url)
    

from requests import get as req_get

from gbpacman.utils.logger import get_global_logger
logger = get_global_logger()


def ping_url(url: str):
    """Performs a get request to given url and returns a response object

    Args:
        url(str): url to which the get request to be sent

    Returns:
        object(Request)
    """
    #logger.debug("pinging url %s"%url)
    return req_get(url)


def get_packages_list():
    pass


def install_package():
    pass


def uninstall_package():
    pass

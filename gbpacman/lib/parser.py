from bs4 import BeautifulSoup
from gbpacman.utils.logger import get_global_logger
logger = get_global_logger()


def parse_html_response(response, parser="html.parser"):
    return BeautifulSoup(response.text, parser)


def get_direct_children(tag):
    return tag.find_all(recursive=False)


def extract(response, filter_fn=None, *args, **kwargs):
    try:
        if filter_fn is None:
            raise ValueError("filter_fn is required")
        soup = parse_html_response(response)
        return soup.find_all(filter_fn, *args, **kwargs)
    except ValueError:
        raise


"""
    # logger.debug(soup)
    # return soup.find_all("div", string=r"Search results .*", attrs={"class": "card mb-3"})
    return soup.find_all("td", string=r"A terminal multiplexer")
    # return soup.find_all("template", attrs={"class": "mytooltip-content"})
"""


def extract_package_table(parent_tag):
    title_tag, table_container_tag = get_direct_children(parent_tag)
    #title_text = title_tag.get_text(strip=True)
    table_tag = table_container_tag.table

    return title_tag, table_tag


def get_children_of_type(tag, **attrs):
    return tag.find_all(**attrs)

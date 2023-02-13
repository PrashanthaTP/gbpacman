from collections import namedtuple
from bs4 import BeautifulSoup
from re import (search as re_search,
                match as re_match,
                IGNORECASE as re_IGNORECASE)
from gbpacman.utils.logger import get_global_logger
logger = get_global_logger()


PackageInfo = namedtuple(
    "PackageInfo", ["name", "description", "link", "version"])

Link = namedtuple("Link", ["name", "href"])


def parse_html_response(response, parser="html.parser"):
    return BeautifulSoup(response.text, parser)


def get_direct_children(tag):
    return tag.find_all(recursive=False)

# TODO: find_all returns a list
# but in most of the cases we expect only one result
# so it makes sense to return the expected found item
# rather a list of single item


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


def get_package_table(parent_tag):
    title_tag, table_container_tag = get_direct_children(parent_tag)
    # title_text = title_tag.get_text(strip=True)
    table_tag = table_container_tag.table

    return title_tag, table_tag


def get_children_of_type(tag, **attrs):
    return tag.find_all(**attrs)


def get_columns(row_tag, **attrs):
    cols = get_children_of_type(row_tag, **attrs)
    return [col.get_text() for col in cols]


def get_packages_list(table_tag):

    # table_row_headings = get_children_of_type(table_tag.thead,
    #                                          **{"name": "th"})
    # package_rows = [[row_heading.get_text()
    #                 for row_heading in table_row_headings]]
    package_rows = []

    for row in get_children_of_type(table_tag.tbody,
                                    **{"name": "tr"}):
        name_tag, version, description = get_children_of_type(row,
                                                              **{"name": "td"})
        link = name_tag.a["href"]
        package_rows.append(PackageInfo(name_tag.get_text(strip=True),
                                        description.get_text(strip=True),
                                        link,
                                        version.get_text(strip=True)
                                        )
                            )
    return package_rows


# to be removed
# TODO: implement : depracated wrapper
def get_package_info_page_link(package_page):
    def is_base_package_link(tag):
        prev_sibling = tag.find_previous_sibling()
        if prev_sibling is None:
            return False
        prev_heading = re_search(r".*Binary Packages\s?:?\s?.*",
                                 prev_sibling.get_text(),
                                 re_IGNORECASE)
        return tag.name == "dd"  \
            and prev_sibling.name == "dt"\
            and prev_heading is not None

    soup = parse_html_response(package_page)
    return soup.find(is_base_package_link)


def get_curr_package_links(ul):
    links = []
    for li in ul.find_all('li'):
        links.append(Link(li.get_text(strip=True), li.a['href']))
    return links


def get_download_link(tag):
    return Link(name=tag.get_text(strip=True), href=tag['href'])

def make_package(url):
    package_name = None
    package_version = None
    package_name_match = re_match(r'(^\w+)',url.split("/")[-1])
    package_version_match = re_match(r'(\w*)-((\d*\.)*(\d*)(-\d*)?)-x\d',
                                     url.split("/")[-1])
    if package_name_match is None:
        raise ValueError(f"Package {url.split('/')[-1]} couldn't be parsed to extract the package name.\nGiven url {url}")
    else:
        package_name=package_name_match.group(1)

    if package_version_match is None:
        raise ValueError(f"Url of package {package_name} couldn't be parsed to extract the package version.\nGiven url {url}")
    else:
        package_version = package_version_match.group(2)

    return PackageInfo(name=package_name,
                       description="",
                       link=url,
                       version=package_version)

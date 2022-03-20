import os
import unittest
from plogger import get_logger

from gbpacman.lib import parser, calls, filters, api
from gbpacman.utils.utils import print_attributes
url = "https://packages.msys2.org"

logger = get_logger(__name__)


def get_response(package_name="tmux"):
    query = f"{url}/search?q={package_name}"
    response = calls.ping_url(query)
    return response


def get_zip_file_link(package_name, version, file_extension="tar.zst", arch="x86_64"):
    """
    https://mirror.msys2.org/msys/x86_64/libutil-linux-2.35.2-1-x86_64.pkg.tar.zst
    """
    base = "https://mirror.msys2.org/msys/x86_64"

    return f"{base}/{package_name}-{version}-{arch}.pkg.{file_extension}"


class TestParser(unittest.TestCase):
    def test_html_parser_with_error(self):
        response = get_response()
        with self.assertRaises(ValueError):
            excerpt = parser.extract(response)

    def test_html_parser(self):
        response = get_response()
        exerpt = parser.extract(response, filters.is_search_table, attrs={
                                "class": "card mb-3"}, limit=1)
        direct_children = parser.get_direct_children(exerpt[0])
        self.assertEqual(len(direct_children), 2)

    def test_extract_table(self):
        response = get_response()
        target_tag = parser.extract(response,
                                    filters.is_search_table,
                                    attrs={"class": "card mb-3"},
                                    limit=1)[0]
        exerpt = parser.get_package_table(target_tag)
        self.assertEqual(len(exerpt), 2)
        self.assertNotIn(None, exerpt)

    def test_get_children_of_type(self):
        response = get_response()
        target_tag = parser.extract(response,
                                    filters.is_search_table,
                                    attrs={"class": "card mb-3"},
                                    limit=1)[0]
        title, table = parser.get_package_table(target_tag)
        headings = parser.get_children_of_type(table.thead, **{"name": "th"})
        self.assertEqual(len(headings), 3)

    def test_get_columns(self):
        response = get_response()
        target_tag = parser.extract(response,
                                    filters.is_search_table,
                                    attrs={"class": "card mb-3"},
                                    limit=1)[0]
        _, table = parser.get_package_table(target_tag)
        cols = parser.get_columns(table.thead, **{"name": "th"})
        self.assertEqual(cols, ["Base Package", "Version", "Description"])

    def test_get_packages_list(self):
        response = get_response()
        target_tag = parser.extract(response,
                                    filters.is_search_table,
                                    attrs={"class": "card mb-3"},
                                    limit=1)[0]
        _, table = parser.get_package_table(target_tag)
        packages_list = parser.get_packages_list(table)
        self.assertEqual(len(packages_list), 1)
        for package in packages_list:
            self.assertTrue(isinstance(package.name, str),
                            "Each package must have a name")
            self.assertTrue(isinstance(package.link, str),
                            "Each package must have a link")
            self.assertTrue(isinstance(package.description, str),
                            "Each package must have a description")
            self.assertTrue(isinstance(package.version, str),
                            "Each package must have version info")

    def test_get_packages_list_container(self):
        response = get_response("util-linux")
        target_tag = parser.extract(response,
                                    filters.is_search_table,
                                    attrs={"class": "card mb-3"},
                                    limit=1)[0]
        _, table = parser.get_package_table(target_tag)
        packages_list = parser.get_packages_list(table)
        self.assertEqual(len(packages_list), 1)
        for package in packages_list:
            package_page = calls.ping_url(package.link)
            dd_tag = parser.extract(package_page,
                                    filters.is_base_package_link,
                                    limit=1)[0]
            self.assertEqual(dd_tag.name, "dd")

    def test_get_package_link(self):
        response = get_response("util-linux")
        target_tag = parser.extract(response,
                                    filters.is_search_table,
                                    attrs={"class": "card mb-3"},
                                    limit=1)[0]
        _, table = parser.get_package_table(target_tag)
        packages_list = parser.get_packages_list(table)
        self.assertEqual(len(packages_list), 1)
        for package in packages_list:
            package_page = calls.ping_url(package.link)
            dd_tag = parser.extract(package_page,
                                    filters.is_base_package_link,
                                    limit=1)[0]
            self.assertEqual(dd_tag.name, "dd")
            links = parser.get_curr_package_links(dd_tag.ul)
            num_expected_links = 3
            self.assertEqual(len(links), num_expected_links)

    def test_extract_package_file_link(self):
        response = get_response("util-linux")
        target_tag = parser.extract(response,
                                    filters.is_search_table,
                                    attrs={"class": "card mb-3"},
                                    limit=1)[0]
        _, table = parser.get_package_table(target_tag)
        packages_list = parser.get_packages_list(table)
        self.assertEqual(len(packages_list), 1)
        for package in packages_list:
            package_page = calls.ping_url(package.link)
            dd_tag = parser.extract(package_page,
                                    filters.is_base_package_link,
                                    limit=1)[0]
            self.assertEqual(dd_tag.name, "dd")
            links = parser.get_curr_package_links(dd_tag.ul)

            download_page = calls.ping_url(links[0].href)

            file_download_tag = parser.extract(download_page,
                                               filters.is_download_link,
                                               limit=None)
            self.assertEqual(len(file_download_tag), 1)
            file_download_link = parser.get_download_link(file_download_tag[0])
            expected_link = get_zip_file_link(links[0].name, "2.35.2-1")
            self.assertEqual(file_download_link.name, expected_link)
            self.assertEqual(file_download_link.href, expected_link)

    def test_download_file(self):
        response = get_response("util-linux")
        target_tag = parser.extract(response,
                                    filters.is_search_table,
                                    attrs={"class": "card mb-3"},
                                    limit=1)[0]
        _, table = parser.get_package_table(target_tag)
        packages_list = parser.get_packages_list(table)
        self.assertEqual(len(packages_list), 1)
        for package in packages_list:
            package_page = calls.ping_url(package.link)
            dd_tag = parser.extract(package_page,
                                    filters.is_base_package_link,
                                    limit=1)[0]
            self.assertEqual(dd_tag.name, "dd")
            links = parser.get_curr_package_links(dd_tag.ul)

            download_page = calls.ping_url(links[0].href)

            file_download_tag = parser.extract(download_page,
                                               filters.is_download_link,
                                               limit=None)
            self.assertEqual(len(file_download_tag), 1)
            file_download_link = parser.get_download_link(file_download_tag[0])
            expected_link = get_zip_file_link(links[0].name, "2.35.2-1")
            self.assertEqual(file_download_link.name, expected_link)
            self.assertEqual(file_download_link.href, expected_link)

            api.download_file(file_download_link.href, download_dir="out")
            filename = file_download_link.href.split("/")[-1]
            self.assertTrue(os.path.isfile(os.path.join("out", filename)))

    def test_unzip(self):
        downloaded_file = os.path.join(
            "out", "libutil-linux-2.35.2-1-x86_64.pkg.tar.zst")
        self.assertTrue(os.path.isfile(downloaded_file))
        api.unzip_file(downloaded_file, "out")


if __name__ == "__main__":
    unittest.main(verbosity=2)

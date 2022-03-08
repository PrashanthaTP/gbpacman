import unittest
from plogger import get_logger

from gbpacman.lib import parser, calls, filters
from gbpacman.utils.utils import print_attributes
url = "https://packages.msys2.org"

logger = get_logger(__name__)


def get_response(package_name="tmux"):
    query = f"{url}/search?q={package_name}"
    response = calls.ping_url(query)
    return response


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
        exerpt = parser.extract_package_table(target_tag)
        self.assertEqual(len(exerpt), 2)
        self.assertNotIn(None, exerpt)

    def test_get_children_of_type(self):
        response = get_response()
        target_tag = parser.extract(response,
                                    filters.is_search_table,
                                    attrs={"class": "card mb-3"},
                                    limit=1)[0]
        title, table = parser.extract_package_table(target_tag)
        headings = parser.get_children_of_type(table.thead, **{"name": "th"})
        self.assertEqual(len(headings), 3)

    def test_get_columns(self):
        response = get_response()
        target_tag = parser.extract(response,
                                    filters.is_search_table,
                                    attrs={"class": "card mb-3"},
                                    limit=1)[0]
        _, table = parser.extract_package_table(target_tag)
        cols = parser.get_columns(table.thead, **{"name": "th"})
        self.assertEqual(cols, ["Base Package", "Version", "Description"])

    def test_get_packages_list(self):
        response = get_response()
        target_tag = parser.extract(response,
                                    filters.is_search_table,
                                    attrs={"class": "card mb-3"},
                                    limit=1)[0]
        _, table = parser.extract_package_table(target_tag)
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

    def test_get_packages_list(self):
        response = get_response("util-linux")
        target_tag = parser.extract(response,
                                    filters.is_search_table,
                                    attrs={"class": "card mb-3"},
                                    limit=1)[0]
        _, table = parser.extract_package_table(target_tag)
        packages_list = parser.get_packages_list(table)
        self.assertEqual(len(packages_list), 1)
        for package in packages_list:
            package_page = calls.ping_url(package.link)
            dd_tag = parser.get_package_info_page_link(package_page)
            self.assertEqual(dd_tag.name, "dd")


if __name__ == "__main__":
    unittest.main(verbosity=2)

import unittest
from plogger import get_logger

from gbpacman.lib import parser, calls, filters
from gbpacman.utils.utils import print_attributes
url = "https://packages.msys2.org"

logger = get_logger(__name__)


def get_response():
    query = f"{url}/search?q=tmux"
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


if __name__ == "__main__":
    unittest.main(verbosity=2)

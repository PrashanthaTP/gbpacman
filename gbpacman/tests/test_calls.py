import unittest
from gbpacman.lib.calls import ping_url

URL = "https://packages.msys2.org"
github = "https://api.github.com"
URLS = [URL]

SUCCESS_CODE = 200


class TestCalls(unittest.TestCase):
    def test_ping_url(self):
        for url in URLS:
            res = ping_url(url)
            self.assertEqual(res.status_code, SUCCESS_CODE)
            print(res.status_code)


if __name__ == "__main__":
    unittest.main(verbosity=2)

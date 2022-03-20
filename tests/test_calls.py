import unittest
from plogger import get_logger
from gbpacman.lib.calls import ping_url

URL = "https://packages.msys2.org"
github = "https://api.github.com"
URLS = [URL]

SUCCESS_CODE = 200

logger = get_logger(__name__)


class TestCalls(unittest.TestCase):
    def test_ping_url(self):
        for url in URLS:
            res = ping_url(url)
            self.assertEqual(res.status_code, SUCCESS_CODE)
            if(res.status_code == SUCCESS_CODE):
                return
            logger.error("Testing ping url failed with response code %s"
                         % res.status_code)


if __name__ == "__main__":
    unittest.main(verbosity=2)

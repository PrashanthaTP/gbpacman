import unittest
from plogger import get_logger

from gbpacman import settings

logger = get_logger(__name__)


class TestCalls(unittest.TestCase):
    def test_settings(self):
        print(settings)


if __name__ == "__main__":
    unittest.main(verbosity=2)

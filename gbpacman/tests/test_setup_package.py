import os
import unittest
from plogger import get_logger

from gbpacman.lib import setup_package

url = "https://packages.msys2.org"

logger = get_logger(__name__)


class TestSetup(unittest.TestCase):
    def setUp(self):
        super().__init__()
        self.out_dir = "out"
        #self.zstd_filename = "zstd-1.5.2.tar.gz"
        self.zstd_filename = "zstd-1.5.2-win64.zip"

    def test_download_zstd(self):

        zstd_fullpath = os.path.join(self.out_dir, self.zstd_filename)
        setup_package.download_zstd()
        self.assertTrue(os.path.isfile(zstd_fullpath))

    def test_unzip_zstd(self):
        zstd_fullpath = os.path.join(
            self.out_dir, self.zstd_filename.strip("zip"))
        setup_package.unzip_zstd()
        self.assertTrue(os.path.isfile(zstd_fullpath))


if __name__ == "__main__":
    unittest.main(verbosity=2)

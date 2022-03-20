import os
import unittest
from plogger import get_logger

from gbpacman.lib import setup_package
from gbpacman.config import settings

url = "https://packages.msys2.org"

logger = get_logger(__name__)


class TestSetup(unittest.TestCase):
    def setUp(self):
        super().__init__()
        self.bin_dir = os.path.join(settings["BASE_DIR"], "bin")
        #self.zstd_filename = "zstd-1.5.2.tar.gz"
        self.zstd_folder_name = os.path.basename(
            settings["exe"]["zstd_url_windows"])

    def test_download_zstd(self):

        zstd_fullpath = os.path.join(self.bin_dir, self.zstd_folder_name)
        setup_package.download_zstd()
        self.assertTrue(os.path.isfile(zstd_fullpath))

    def test_unzip_zstd(self):
        zstd_exe = os.path.join(self.bin_dir,
                                self.zstd_folder_name.rstrip(".zip"),
                                "zstd.exe")
        setup_package.unzip_zstd()
        self.assertTrue(os.path.isfile(zstd_exe), f"Needed {zstd_exe}")


if __name__ == "__main__":
    unittest.main(verbosity=2)

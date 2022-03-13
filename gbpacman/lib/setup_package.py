from os import path as os_path
from gbpacman.lib.api import download_file
from gbpacman.utils import unzip_file, get_global_logger
from gbpacman import settings


logger = get_global_logger()

ZSTD_INSTALLATION_DIR = settings["exe"]["zstd_installation_dir"]
ZSTD_URL_WINDOWS = settings["exe"]["zstd_url_windows"]


def download_zstd():
    try:
        download_file(url=ZSTD_URL_WINDOWS, download_dir=ZSTD_INSTALLATION_DIR)
    except Exception as _:
        raise


def remove_zip_extension(path):
    extensions = ["zip", "tar.gz"]
    for ext in extensions:
        path = path.rstrip(f".{ext}")

    return path


def unzip_zstd():
    zstd_zip_filename = os_path.basename(ZSTD_URL_WINDOWS)
    zstd_location = os_path.join(ZSTD_INSTALLATION_DIR,
                                 zstd_zip_filename)
    unzipped_zstd_folder = remove_zip_extension(zstd_zip_filename)
    try:
        unzip_file(zip_file=zstd_location,
                   target_dir=ZSTD_INSTALLATION_DIR,
                   logger=logger)
        settings.set("exe",
                     {**settings["exe"],
                      "zstd_exe": os_path.join(unzipped_zstd_folder, "zstd.exe")
                      })
    except Exception:
        raise


def run_setup():
    download_zstd()
    unzip_zstd()

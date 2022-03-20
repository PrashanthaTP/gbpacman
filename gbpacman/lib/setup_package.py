import tarfile
from zipfile import ZipFile

from os import path as os_path
import shutil

from gbpacman.lib.api import download_file
from gbpacman.utils import get_global_logger
from gbpacman.config import settings


logger = get_global_logger()

#ZSTD_INSTALLATION_DIR = settings["exe"]["zstd_installation_dir"]
ZSTD_INSTALLATION_DIR = settings["temp_dir"]
ZSTD_URL_WINDOWS = settings["exe"]["zstd_url_windows"]


def unzip_file(zip_file, target_dir, logger=None):
    if logger:
        logger.debug("unzipping %s" % (zip_file))
    if zip_file.endswith("tar.gz"):
        tar = tarfile.open(zip_file, "r:gz")
        tar.extractall(path=target_dir)
        tar.close()

    elif zip_file.endswith("zip"):
        with ZipFile(zip_file, 'r') as zipref:
            zipref.extractall(target_dir)


def download_zstd():
    try:
        download_file(url=ZSTD_URL_WINDOWS,
                      download_dir=ZSTD_INSTALLATION_DIR)
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

        shutil.copy2(os_path.join(ZSTD_INSTALLATION_DIR,
                                  unzipped_zstd_folder,
                                  "zstd.exe"),
                     settings["exe"]["zstd_exe"])
        # settings.set("exe",
        #             {**settings["exe"],
        #              "zstd_exe": os_path.join(unzipped_zstd_folder, "zstd.exe")
        #              }, write_file=False)
    except Exception:
        raise


def run_setup():
    if os_path.isfile(settings["exe"]["zstd_exe"]):
        return
    logger.debug("Downloading zstd...")
    download_zstd()
    unzip_zstd()

from os import (path as os_path,
                listdir as os_listdir,
                makedirs as os_makedirs)
import shutil
import tarfile
from zipfile import ZipFile

from .os_calls import run_cmd
from .logger import get_global_logger
from gbpacman.config import settings


def unzip_tar(zip_file, target_dir, mode="r:"):
    with tarfile.open(zip_file, mode) as tar:
        tar.extractall(path=target_dir)

# TODD: do something recursive


def unzip_file(zip_file, target_dir, logger=None):
    temp_target_dir = zip_file.split(".")[0]
    target_dir = os_path.join(target_dir, temp_target_dir)
    os_makedirs(target_dir, exist_ok=True)

    def get_unzip_filepath(zip_name):
        nonlocal target_dir
        return os_path.join(target_dir, zip_name)

    ext = ""
    if logger:
        logger.debug("unzipping %s" % (zip_file))
    else:
        logger = get_global_logger()

    if zip_file.endswith("tar"):
        unzip_tar(zip_file,
                  target_dir=os_path.join(target_dir, zip_file.rstrip(".tar")),
                  mode="r:")

        ext = "tar"
    if zip_file.endswith("tar.gz"):
        unzip_tar(zip_file, target_dir, mode="r:gz")
        ext = "tar.gz"

    elif zip_file.endswith("tar.xz"):
        unzip_tar(zip_file, target_dir, mode="r:xz")
        ext = "tar.xz"

    elif zip_file.endswith("zip"):
        with ZipFile(zip_file, 'r') as zipref:
            zipref.extractall(target_dir)

        ext = "zip"

    elif zip_file.endswith("tar.zst"):
        from gbpacman.lib.setup_package import run_setup
        run_setup()
        zstd_exe = settings["exe"]["zstd_exe"]
        logger.debug("Unzipping with zstd...")
        res = run_cmd([zstd_exe, "-d", zip_file],
                      shell=False, capture_output=True)

        assert(res.returncode in [0, 1])
        if res.returncode == 1:
            logger.warning(res.stderr)
        unzip_file(zip_file.rstrip(".zst"),
                   target_dir=target_dir, logger=logger)

        ext = "tar.zst"
    # to handle cases where the files are extracted directly to target dir
    # instead of extracting inside a new folder with the zip_file name
    possible_unzipped_folder = zip_file.rstrip(ext)
    unzipped_dirs = os_listdir(target_dir)
    if possible_unzipped_folder in unzipped_dirs:
        # unzipping resulted in new folder
        return get_unzip_filepath(possible_unzipped_folder)
    else:
        return target_dir  # files are directly extracted to given directory


# TODO : move instead of copying?
def recursive_copy(from_dir, to_dir):
    """
    https://stackoverflow.com/questions/12683834/how-to-copy-directory-recursively-in-python-and-overwrite-all
    """
    copied_files = []

    def copy_files(from_d, to_d):
        nonlocal copied_files
        if os_path.isdir(from_d):
            os_makedirs(to_d, exist_ok=True)
            files = os_listdir(from_d)
            for file in files:
                copy_files(os_path.join(from_d, file),
                           os_path.join(to_d, file))

        else:
            try:
                shutil.copy2(from_d, to_d)
            except shutil.SameFileError:
                shutil.copyfile(from_d, to_d)

            copied_files.append(to_d)
    copy_files(from_dir, to_dir)
    return copied_files

from datetime import datetime
from os import (path as os_path,
                makedirs as os_makedirs)

from gbpacman.utils import get_global_logger
from gbpacman.lib import calls, parser, filters
from gbpacman.config import settings


from gbpacman.utils import unzip_file, recursive_copy
logger = get_global_logger()


TEMP_DIR = settings["temp_dir"]
INSTALLTION_DIR = settings["installation_dir"]


def download_file(url, download_dir: str):
    """
    https://stackoverflow.com/a/53153505/12988588
    """
    response = calls.ping_url(url)
    filename = url.split("/")[-1]

    if len(download_dir) > 0:
        os_makedirs(download_dir, exist_ok=True)
    out_filepath = os_path.join(download_dir, filename)
    with open(out_filepath, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk is None:
                continue
            file.write(chunk)
    logger.info("File downloaded : %s" %
                (out_filepath))

    return out_filepath


def get_zip_file_name(package_name, version, file_extension="tar.zst", arch="x86_64"):
    """
    https://mirror.msys2.org/msys/x86_64/libutil-linux-2.35.2-1-x86_64.pkg.tar.zst
    """

    return f"{package_name}-{version}-{arch}.pkg.{file_extension}"


def check_if_already_downloaded(package_zip_filename):
    filepath = os_path.join(TEMP_DIR, package_zip_filename)
    if os_path.isfile(filepath):
        return filepath
    else:
        return None


def get_package_files_infofile(unzipped_folder):
    installation_info_dir = settings["installation_info_dir"]
    return os_path.join(installation_info_dir,
                        f"{os_path.basename(unzipped_folder)}.txt")


def is_already_installed(package_name):
    installed_packages_list = get_installed_packages()
    for package in installed_packages_list:
        curr_package_name, package_info_file = package.split(
            "#").strip(" ")
        if package_name == curr_package_name:
            return True
    return False


def check_if_already_installed(package_name):
    installed_packages_list = get_installed_packages()
    for package in installed_packages_list:
        curr_package_name, package_info_file = package.strip(" ").split("#")
        if package_name == curr_package_name.strip():
            #logger.info("Package %s is already installed" % (package_name))
            return package_info_file.strip()
    return None


def get_installed_packages():
    all_packages_txt = os_path.join(settings["installation_info_dir"],
                                    "all.txt")
    if not os_path.isfile(all_packages_txt):
        return []
    with open(all_packages_txt, 'r') as file:
        return set(file.readlines())


def download_package(package):
    package_info_file = check_if_already_installed(package.name)
    if package_info_file is not None:
        with open(package_info_file, 'r') as file:
            logger.debug("%s already installed @ %s" %
                         (package.name, file.readline()))
            return None

    package_page = calls.ping_url(package.link)
    dd_tag = parser.extract(package_page,
                            filters.is_base_package_link,
                            limit=1)[0]
    # self.assertEqual(dd_tag.name, "dd")
    links = parser.get_curr_package_links(dd_tag.ul)

    download_page = calls.ping_url(links[0].href)

    file_download_tag = parser.extract(download_page,
                                       filters.is_download_link,
                                       limit=None)
    # self.assertEqual(len(file_download_tag), 1)
    file_download_link = parser.get_download_link(file_download_tag[0])

    file_path = check_if_already_downloaded(
        os_path.basename(file_download_link.href))
    if file_path is not None:
        logger.debug(f"Skipping downloading for package : {package.name}")
        logger.debug(
            f"{os_path.basename(file_download_link.href)} is already downloaded.")
        return file_path

    file_name = download_file(file_download_link.href, download_dir=TEMP_DIR)
    return os_path.join(file_name)


def install_downloaded_package(package_file_path, package_name):
    package_info_file = check_if_already_installed(package_name)
    if package_info_file is not None:
        with open(package_info_file, 'r') as file:
            logger.debug("%s already downloaded and installed @ %s" %
                         (package_name, file.readline()))
            return package_info_file

    unzipped_folder = unzip_file(package_file_path, target_dir=TEMP_DIR)

    """
    package_files_info_file = get_package_files_infofile(unzipped_folder)
    if os_path.isfile(package_files_info_file):
        with open(package_files_info_file, 'r') as file:
            logger.debug("Package already installed @ %s" % (file.readline()))
            return
    """
    copied_files = recursive_copy(from_dir=unzipped_folder,
                                  to_dir=INSTALLTION_DIR)
    package_files_infofile = get_package_files_infofile(unzipped_folder)
    with open(package_files_infofile, 'w') as file:
        file.write(f"{package_name} :")
        file.write(str(datetime.now()))
        file.write("\n")
        for path in copied_files:
            file.write(path)
            file.write("\n")

    with open(os_path.join(settings["installation_info_dir"], "all.txt"), "a") as file:
        file.writelines([f"{package_name} # {package_files_infofile}\n"])

    logger.debug("List of downloaded files written to %s" %
                 (package_files_infofile))

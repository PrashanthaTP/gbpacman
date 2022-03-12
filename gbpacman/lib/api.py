import os
from zipfile import ZipFile
from .calls import ping_url
from gbpacman.utils import get_global_logger

logger = get_global_logger()


def download_file(url, download_dir: str):
    """
    https://stackoverflow.com/a/53153505/12988588
    """
    response = ping_url(url)
    filename = url.split("/")[-1]

    if len(download_dir) > 0:
        os.makedirs(download_dir, exist_ok=True)
    out_filepath = os.path.join(download_dir, filename)
    with open(out_filepath, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk is None:
                continue
            file.write(chunk)
    logger.info("File downloaded : %s" %
                (out_filepath))


def unzip_file(zip_file, target_dir):

    with ZipFile(zip_file, 'r') as zipref:
        zipref.extractall(target_dir)

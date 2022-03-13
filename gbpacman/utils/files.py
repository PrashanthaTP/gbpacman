import tarfile
from zipfile import ZipFile


def unzip_file(zip_file, target_dir, logger=None):
    if logger:
        logger.debug("unzipping %s" % (zip_file))
    if zip_file.endswith("tar.gz"):
        tar = tarfile.open(zip_file, "r:gz")
        tar.extractall(path=target_dir)
        tar.close()

    else:
        with ZipFile(zip_file, 'r') as zipref:
            zipref.extractall(target_dir)

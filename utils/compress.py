import gzip
import shutil


def gzip_file(source: str, target: str):
    with open(source, "rb") as f_in:
        with gzip.open(target, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

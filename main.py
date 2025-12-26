import os
from config import DB_ENGINE, DB_CONFIG, R2_CONFIG
from utils.compress import gzip_file
from storage.r2_storage import R2Storage

from databases.mysql import MySQLBackup
from databases.postgres import PostgresBackup

TMP = "./tmp"
os.makedirs(TMP, exist_ok=True)


def get_db_backup():
    if DB_ENGINE == "mysql":
        return MySQLBackup(DB_CONFIG)
    if DB_ENGINE == "postgres":
        return PostgresBackup(DB_CONFIG)
    raise ValueError("DB_ENGINE no soportado")


def main():
    db = get_db_backup()
    storage = R2Storage(R2_CONFIG)

    filename = db.filename()
    dump_path = f"{TMP}/{filename}"
    gz_path = f"{dump_path}.gz"

    db.dump(dump_path)
    gzip_file(dump_path, gz_path)

    storage.upload(gz_path, f"backups/{gz_path.split('/')[-1]}")

    os.remove(dump_path)
    os.remove(gz_path)


if __name__ == "__main__":
    main()

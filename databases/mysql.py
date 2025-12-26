import subprocess
import datetime
from .base import DatabaseBackup


class MySQLBackup(DatabaseBackup):

    def filename(self):
        ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"{self.config['name']}_{ts}.sql"

    def dump(self, output_file: str):
        cmd = [
            "mysqldump",
            f"-h{self.config['host']}",
            f"-P{self.config['port']}",
            f"-u{self.config['user']}",
            f"-p{self.config['password']}",
            "--single-transaction",
            "--routines",
            "--triggers",
            self.config["name"]
        ]

        with open(output_file, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, check=True)

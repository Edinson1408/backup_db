import subprocess
import datetime
import os
import shutil
from .base import DatabaseBackup


class MySQLBackup(DatabaseBackup):

    def filename(self):
        ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"{self.config['name']}_{ts}.sql"

    def _find_mysqldump(self):
        """Encuentra la ruta de mysqldump en el sistema"""
        # Primero intenta encontrar mysqldump en el PATH
        mysqldump_path = shutil.which("mysqldump")
        if mysqldump_path:
            return mysqldump_path

        # Rutas comunes de MySQL en Windows
        common_paths = [
            r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
            r"C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqldump.exe",
            r"C:\Program Files\MySQL\MySQL Server 5.7\bin\mysqldump.exe",
            r"C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysqldump.exe",
            r"C:\Program Files (x86)\MySQL\MySQL Server 5.7\bin\mysqldump.exe",
            r"C:\xampp\mysql\bin\mysqldump.exe",
            r"C:\wamp64\bin\mysql\mysql8.0.31\bin\mysqldump.exe",
        ]

        for path in common_paths:
            if os.path.exists(path):
                return path

        raise FileNotFoundError(
            "No se pudo encontrar mysqldump. "
            "Asegúrate de que MySQL esté instalado y mysqldump esté en el PATH, "
            "o instala MySQL en una de las rutas estándar."
        )

    def dump(self, output_file: str):
        mysqldump_cmd = self._find_mysqldump()

        # Configurar variables de entorno para evitar el warning de seguridad
        env = os.environ.copy()
        env['MYSQL_PWD'] = self.config['password']

        cmd = [
            mysqldump_cmd,
            f"-h{self.config['host']}",
            f"-P{self.config['port']}",
            f"-u{self.config['user']}",
            "--single-transaction",
            "--routines",
            "--triggers",
            self.config["name"]
        ]

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE,
                                        env=env, check=True, text=True)
            print(f"✅ Dump de MySQL creado exitosamente: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al crear el dump de MySQL:")
            print(f"   Comando: {' '.join(cmd)}")
            print(f"   Error: {e.stderr}")
            raise

import os
from config import DB_ENGINE, DB_CONFIG, R2_CONFIG
from utils.compress import gzip_file
from storage.r2_storage import R2Storage

from databases.mysql import MySQLBackup
# from databases.postgres import PostgresBackup

TMP = "./tmp"
os.makedirs(TMP, exist_ok=True)


def get_db_backup():
    if DB_ENGINE == "mysql":
        return MySQLBackup(DB_CONFIG)
    # if DB_ENGINE == "postgres":
    #     return PostgresBackup(DB_CONFIG)
    raise ValueError("DB_ENGINE no soportado")


def main():
    print("🚀 Iniciando proceso de backup de base de datos...")

    try:
        # Validar configuración
        if not DB_ENGINE:
            raise ValueError("DB_ENGINE no está configurado en .env")

        print(f"📊 Motor de BD: {DB_ENGINE}")
        print(f"🗄️  Base de datos: {DB_CONFIG.get('name', 'N/A')}")
        print(f"🏠 Host: {DB_CONFIG.get('host', 'N/A')}")

        db = get_db_backup()
        storage = R2Storage(R2_CONFIG)

        filename = db.filename()
        dump_path = f"{TMP}/{filename}"
        gz_path = f"{dump_path}.gz"

        print(f"\n📁 Archivos:")
        print(f"   Dump: {dump_path}")
        print(f"   Comprimido: {gz_path}")

        # Crear dump
        print(f"\n🔄 Creando dump de la base de datos...")
        db.dump(dump_path)

        # Comprimir
        print(f"🗜️  Comprimiendo archivo...")
        gzip_file(dump_path, gz_path)

        # Verificar tamaños
        original_size = os.path.getsize(dump_path)
        compressed_size = os.path.getsize(gz_path)
        compression_ratio = (1 - compressed_size / original_size) * 100
        print(f"✅ Compresión completada:")
        print(f"   Original: {original_size:,} bytes")
        print(f"   Comprimido: {compressed_size:,} bytes")
        print(f"   Reducción: {compression_ratio:.1f}%")

        # Subir a R2
        storage.upload(gz_path, f"backup/{gz_path.split('/')[-1]}")

        # Limpiar archivos temporales
        print(f"\n🧹 Limpiando archivos temporales...")
        os.remove(dump_path)
        os.remove(gz_path)
        print(f"✅ Archivos temporales eliminados")

        print(f"\n🎉 ¡Backup completado exitosamente!")

    except Exception as e:
        print(f"\n❌ Error durante el proceso de backup:")
        print(f"   {str(e)}")
        print(f"\n💡 Verifica:")
        print(f"   - Que el archivo .env esté configurado correctamente")
        print(f"   - Que MySQL esté disponible y las credenciales sean correctas")
        print(f"   - Que las credenciales de R2 sean válidas y tengan permisos")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)

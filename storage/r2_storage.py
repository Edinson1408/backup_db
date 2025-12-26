import boto3
import os
from botocore.exceptions import ClientError, NoCredentialsError


class R2Storage:

    def __init__(self, config):
        # Validar configuración
        required_keys = ['endpoint', 'access_key', 'secret_key', 'bucket']
        missing_keys = [key for key in required_keys if not config.get(key)]
        if missing_keys:
            raise ValueError(
                f"Faltan configuraciones de R2: {', '.join(missing_keys)}")

        try:
            self.client = boto3.client(
                "s3",
                endpoint_url=config["endpoint"],
                aws_access_key_id=config["access_key"],
                aws_secret_access_key=config["secret_key"],
                region_name="auto",
            )
            self.bucket = config["bucket"]
        except Exception as e:
            raise ValueError(f"Error al inicializar cliente R2: {str(e)}")

    def upload(self, file_path: str, key: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo no existe: {file_path}")

        file_size = os.path.getsize(file_path)
        print(f"📤 Subiendo archivo a R2...")
        print(f"   Archivo: {file_path} ({file_size:,} bytes)")
        print(f"   Destino: {self.bucket}/{key}")

        try:
            self.client.upload_file(
                Filename=file_path,
                Bucket=self.bucket,
                Key=key,
                ExtraArgs={
                    "ContentType": "application/gzip",
                    "ContentDisposition": "attachment"
                }
            )
            print(f"✅ Archivo subido exitosamente a R2: {key}")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AccessDenied':
                print(f"❌ Error de acceso denegado a R2:")
                print(
                    f"   - Verifica que las credenciales (access_key/secret_key) sean correctas")
                print(f"   - Verifica que el bucket '{self.bucket}' exista")
                print(f"   - Verifica que las credenciales tengan permisos de escritura")
            elif error_code == 'NoSuchBucket':
                print(f"❌ El bucket '{self.bucket}' no existe")
            else:
                print(
                    f"❌ Error de R2: {error_code} - {e.response['Error']['Message']}")
            raise
        except NoCredentialsError:
            print(f"❌ No se encontraron credenciales válidas para R2")
            raise
        except Exception as e:
            print(f"❌ Error inesperado al subir a R2: {str(e)}")
            raise

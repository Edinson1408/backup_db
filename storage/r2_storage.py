import boto3


class R2Storage:

    def __init__(self, config):
        self.client = boto3.client(
            "s3",
            endpoint_url=config["endpoint"],
            aws_access_key_id=config["access_key"],
            aws_secret_access_key=config["secret_key"],
            region_name="auto",
        )
        self.bucket = config["bucket"]

    def upload(self, file_path: str, key: str):
        self.client.upload_file(
            Filename=file_path,
            Bucket=self.bucket,
            Key=key,
            ExtraArgs={
                "ContentType": "application/gzip",
                "ContentDisposition": "attachment"
            }
        )

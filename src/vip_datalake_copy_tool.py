from src.model.copying_tool import S3CopyingTool


class VIPDataLakeCopyTool(S3CopyingTool):

    def __init__(self, source_bucket: str, destination_bucket: str, aws_access_key_id: str, aws_secret_access_key: str,
                 retries: int = 3):

        super().__init__(source_bucket, destination_bucket, aws_access_key_id, aws_secret_access_key, retries)

    @property
    def folder_to_scan(self) -> str:
        return "IMOSDL/Hourly"

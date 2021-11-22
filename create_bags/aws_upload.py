from configparser import ConfigParser
from pathlib import Path

import boto3
from botocore.exceptions import ClientError


class S3Uploader(object):
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("local_settings.cfg")
        s3 = boto3.resource(service_name='s3', region_name=self.config["AWS"]["region_name"],
                            aws_access_key_id=self.config["AWS"]["access_key"], aws_secret_access_key=self.config["AWS"]["secret_key"])
        self.bucket = s3.Bucket(self.config["AWS"]["bucket"])

    def upload_pdf_to_s3(self, filepath):
        """Uploads a PDF file to a 'pdf' directory

        Args:
            filepath (Path obj): full filepath to the PDF to upload
        """
        object_name = str(Path("pdfs", filepath.name))
        try:
            self.bucket.upload_file(str(filepath), object_name, ExtraArgs={
                                    'ContentType': "application/pdf"})
            return True
        except ClientError as e:
            raise Exception(f"AWS upload error: {e}")

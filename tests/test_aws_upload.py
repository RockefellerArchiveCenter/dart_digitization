from configparser import ConfigParser

import boto3
from create_bags.aws_upload import S3Uploader
from moto import mock_s3


@mock_s3
def test_upload_pdf_to_s3(tmp_path):
    config = ConfigParser()
    config.read("local_settings.cfg")
    file_to_upload = tmp_path / "test.txt"
    file_to_upload.touch()
    s3 = boto3.resource(service_name='s3', region_name=config["AWS"]["region_name"],
                        aws_access_key_id=config["AWS"]["access_key"], aws_secret_access_key=config["AWS"]["secret_key"])
    s3.create_bucket(Bucket=config["AWS"]["bucket"])
    s3_upload = S3Uploader().upload_pdf_to_s3(file_to_upload)
    assert s3_upload

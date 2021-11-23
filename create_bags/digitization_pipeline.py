import logging
from pathlib import Path
from shutil import rmtree

import shortuuid

from .archivesspace import ArchivesSpaceClient
from .aws_upload import S3Uploader
from .bag_creator import BagCreator
from .helpers import copy_tiff_files, get_access_pdf


class DigitizationPipeline:

    def __init__(self, root_dir, tmp_dir):
        logging.basicConfig(
            datefmt='%m/%d/%Y %I:%M:%S %p',
            filename='bag_creator.log',
            format='%(asctime)s %(message)s',
            level=logging.INFO)
        self.tmp_dir = tmp_dir
        self.root_dir = root_dir
        self.as_client = ArchivesSpaceClient(baseurl=self.config.get(
            "ArchivesSpace", "baseurl"), username=self.config.get(
            "ArchivesSpace", "username"), password=self.config.get(
            "ArchivesSpace", "password"))

    def run(self, rights_ids):
        print("Starting run...")
        refids = [
            d.name for d in Path(
                self.root_dir).iterdir() if Path(
                self.root_dir,
                d).iterdir() and len(
                d.name) == 32]
        for refid in refids:
            try:
                ao_uri = self.as_client.get_uri_from_refid(self.refid)
                dimes_identifier = shortuuid.uuid(ao_uri)
                pdf_path = get_access_pdf(
                    Path(self.root_dir, refid, "service_edited"))
                S3Uploader().upload_pdf_to_s3(
                    pdf_path, f"pdfs/{dimes_identifier}.pdf")
                dir_to_bag = Path(self.tmp_dir, refid)
                logging.info(
                    f"PDF successfully uploaded: {dimes_identifier}.pdf")
                master_tiffs = copy_tiff_files(
                    Path(self.root_dir, refid, "master"), dir_to_bag)
                master_edited_tiffs = []
                if Path(self.root_dir, refid, "master_edited").is_dir():
                    master_edited_tiffs = copy_tiff_files(Path(
                        self.root_dir, refid, "master_edited"), Path(self.tmp_dir, refid, "service"))
                list_of_files = master_tiffs + master_edited_tiffs
                created_bag = BagCreator().run(refid, rights_ids, list_of_files)
                logging.info(f"Bag successfully created: {created_bag}")
                rmtree(dir_to_bag)
                logging.info(f"Directory {dir_to_bag} successfully removed")
            except Exception as e:
                print(e)
                logging.error(f"Error for ref_id {refid}: {e}")

import logging
from pathlib import Path

from .bag_creator import BagCreator
from .helpers import copy_tiff_files, remove_copied_files


class DigitizationPipeline:

    def __init__(self, root_dir, tmp_dir):
        logging.basicConfig(
            datefmt='%m/%d/%Y %I:%M:%S %p',
            filename='bag_creator.log',
            format='%(asctime)s %(message)s',
            level=logging.INFO)
        self.tmp_dir = tmp_dir
        self.root_dir = root_dir

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
                master_tiffs = copy_tiff_files(
                    Path(self.root_dir, refid, "master"), Path(self.tmp_dir, refid))
                master_edited_tiffs = []
                if Path(self.root_dir, refid, "master_edited").is_dir():
                    master_edited_tiffs = copy_tiff_files(Path(
                        self.root_dir, refid, "master_edited"), Path(self.tmp_dir, refid, "service"))
                list_of_files = master_tiffs + master_edited_tiffs
                created_bag = BagCreator().run(refid, rights_ids, list_of_files)
                logging.info(
                    "Bag successfully created: {}".format(created_bag))
                remove_copied_files(list_of_files)
                if Path(self.tmp_dir, refid, "service").is_dir():
                    Path(self.tmp_dir, refid, "service").rmdir()
                Path(self.tmp_dir, refid).rmdir()
                logging.info(
                    "Files successfully removed from {}/{}".format(self.tmp_dir, refid))
            except Exception as e:
                print(e)
                logging.error("Error for ref_id {}: {}".format(refid, e))

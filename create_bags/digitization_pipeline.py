import logging
from pathlib import Path
from shutil import rmtree

from .bag_creator import BagCreator
from .helpers import copy_tiff_files


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
                logging.info(f"Starting {refid}...")
                dir_to_bag = Path(self.tmp_dir, refid)
                master_tiffs = copy_tiff_files(
                    Path(self.root_dir, refid, "master"), dir_to_bag)
                master_edited_tiffs = []
                if Path(self.root_dir, refid, "master_edited").is_dir():
                    master_edited_tiffs = copy_tiff_files(Path(
                        self.root_dir, refid, "master_edited"), Path(self.tmp_dir, refid, "service"))
                list_of_files = master_tiffs + master_edited_tiffs
                logging.info(
                    f"{len(list_of_files)} files copied successfully for {refid}")
                bag_creator = BagCreator()
                logging.info(
                    f"Using DART installation {bag_creator.dart_command} with workflow {bag_creator.workflow}")
                created_bag = bag_creator.run(refid, rights_ids, list_of_files)
                logging.info(f"Bag successfully created: {created_bag}")
                rmtree(dir_to_bag)
                logging.info(f"Directory {dir_to_bag} successfully removed")
            except Exception as e:
                print(e)
                logging.error(f"Error for ref_id {refid}: {e}")

    def debug_run(self, rights_ids):
        '''Does not create bag, instead outputs job params to file'''
        print("Starting run...")
        refids = [
            d.name for d in Path(
                self.root_dir).iterdir() if Path(
                self.root_dir,
                d).iterdir() and len(
                d.name) == 32]
        for refid in refids:
            try:
                logging.info(f"Starting {refid}...")
                dir_to_bag = Path(self.tmp_dir, refid)
                master_tiffs = copy_tiff_files(
                    Path(self.root_dir, refid, "master"), dir_to_bag)
                master_edited_tiffs = []
                if Path(self.root_dir, refid, "master_edited").is_dir():
                    master_edited_tiffs = copy_tiff_files(Path(
                        self.root_dir, refid, "master_edited"), Path(self.tmp_dir, refid, "service"))
                list_of_files = master_tiffs + master_edited_tiffs
                logging.info(
                    f"{len(list_of_files)} files copied successfully for {refid}")
                bag_creator = BagCreator()
                logging.info(
                    f"Using DART installation {bag_creator.dart_command} with workflow {bag_creator.workflow}")
                created_bag = bag_creator.run(
                    refid, rights_ids, list_of_files, create_bag=False)
                logging.info(f"Bag successfully created: {created_bag}")
                rmtree(dir_to_bag)
                logging.info(f"Directory {dir_to_bag} successfully removed")
            except Exception as e:
                print(e)
                logging.error(f"Error for ref_id {refid}: {e}")

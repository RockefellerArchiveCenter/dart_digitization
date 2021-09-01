import logging
from os import listdir
from os.path import isdir, join

from .bag_creator import BagCreator
from .helpers import copy_tiff_files


class DigitizationPipeline:

    def __init__(self, tmp_dir, root_dir):
        logging.basicConfig(
            datefmt='%m/%d/%Y %I:%M:%S %p',
            filename='bag_creator.log',
            format='%(asctime)s %(message)s',
            level=logging.INFO)
        self.tmp_dir = tmp_dir
        self.root_dir = root_dir

    def run(self, rights_ids):
        print("Starting run...")
        refids = [d for d in listdir(self.root_dir) if isdir(
            join(self.root_dir, d)) and len(d) == 32]
        print(refids)
        list_of_created_bags = []
        for refid in refids:
            try:
                master_tiffs = copy_tiff_files(
                    join(self.root_dir, refid, "master"), join(self.tmp_dir, refid))
                print(master_tiffs)
                master_edited_tiffs = []
                if isdir(join(self.root_dir, refid, "master_edited")):
                    master_edited_tiffs = copy_tiff_files(join(
                        self.root_dir, refid, "master_edited"), join(self.tmp_dir, refid, "service"))
                list_of_files = master_tiffs + master_edited_tiffs
                print(list_of_files)
                created_bag = BagCreator().run(refid, rights_ids, list_of_files)
                list_of_created_bags.append(created_bag)
                logging.info(
                    "Bag successfully created: {}".format(created_bag))
            except Exception as e:
                print(e)
                logging.error("Error for ref_id {}: {}".format(refid, e))

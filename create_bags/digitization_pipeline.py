from os import listdir
from os.path import isdir, join

from .bag_creator import BagCreator
from .helpers import copy_tiff_files


class DigitizationPipeline:

    def __init__(self, tmp_dir, root_dir):
        self.tmp_dir = tmp_dir
        self.root_dir = root_dir

    def run(self, rights_ids):
        refids = [d for d in listdir(self.root_dir) if isdir(
            join(self.root_dir, d)) and len(d) == 32]
        list_of_created_bags = []
        for refid in refids:
            master_tiffs = copy_tiff_files(
                join(self.root_dir, refid, "master"), join(self.tmp_dir, refid))
            master_edited_tiffs = []
            if isdir(join(self.root_dir, refid, "master_edited")):
                master_edited_tiffs = copy_tiff_files(join(
                    self.root_dir, refid, "master_edited"), join(self.tmp_dir, refid, "service"))
            list_of_files = master_tiffs + master_edited_tiffs
            created_bags = BagCreator().run(self.tmp_dir, refid, rights_ids, list_of_files)
            list_of_created_bags.append(created_bags)
        return "Bags successfully created: {}".format(list_of_created_bags)

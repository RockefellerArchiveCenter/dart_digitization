import logging
from configparser import ConfigParser

# from .archivesspace import ArchivesSpaceClient


class BagCreator():

    def __init__(self):
        logging.basicConfig(
            datefmt='%m/%d/%Y %I:%M:%S %p',
            filename='bag_creator.log',
            format='%(asctime)s %(message)s',
            level=logging.INFO)
        self.config = ConfigParser()
        self.config.read("local_settings.cfg")
        self.ignore_list = self.config.get("IgnoreList", "ignore_list")

    def create_target_directory(self):
        """docstring for create_target_directory"""
    pass

    def copy_files_to_target_directory(self):
        """docstring for copy_files_to_target_directory"""
    pass

import logging

from configparser import ConfigParser
from .archivesspace import ArchivesSpaceClient


class BagCreator():
    """docstring for BagCreator"""

    def __init__(self):
        logging.basicConfig(
            datefmt='%m/%d/%Y %I:%M:%S %p',
            filename='iiif_preparer.log',
            format='%(asctime)s %(message)s',
            level=logging.INFO)
        self.config = ConfigParser()
        self.config.read("local_settings.cfg")
        self.ignore_list = self.config.get("IgnoreList", "ignore_list")

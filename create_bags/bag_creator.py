import logging
from configparser import ConfigParser
from os import mkdir
from os.path import join

from .archivesspace import ArchivesSpaceClient
from .helpers import format_aspace_date, get_dates


class BagCreator():

    def __init__(self):
        logging.basicConfig(
            datefmt='%m/%d/%Y %I:%M:%S %p',
            filename='bag_creator.log',
            format='%(asctime)s %(message)s',
            level=logging.INFO)
        self.config = ConfigParser()
        self.config.read("local_settings.cfg")
        self.dest_location = self.configet.get("Locations", "dest_location")

    def run(self):
        # directory_to_bag = "some directory"
        self.refid = "some refid"
        self.target_directory = self.create_target_directory()
        as_client = ArchivesSpaceClient(baseurl=self.config.get("ArchivesSpace", "baseurl"), username=self.config.get(
            "ArchivesSpace", "username"), password=self.config.get("ArchivesSpace", "password"))
        ao_uri = as_client.get_ao_uri(self.refid)
        ao_data = as_client.get_ao_data(ao_uri)
        dates = get_dates(ao_data)
        start_date, end_date = format_aspace_date(dates)
        # tag_file = "bag-info.txt"
        # tags = [{"tagName": "start-date", "userValue": start_date},
        #         {"tagName": "end-date", "userValue": end_date}]

    def create_target_directory(self):
        """docstring for create_target_directory"""
        # create directory with name self.refid in self.target_directory
        target_directory = join(self.dest_location, self.refid)
        try:
            mkdir(target_directory)
            return target_directory
        except Exception as e:
            print(e)

    def copy_files_to_target_directory(self):
        """docstring for copy_files_to_target_directory"""
    pass

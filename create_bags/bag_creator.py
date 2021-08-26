import logging
from configparser import ConfigParser

from .archivesspace import ArchivesSpaceClient
from .helpers import create_tag, format_aspace_date, get_dates


class BagCreator:

    def __init__(self):
        logging.basicConfig(
            datefmt='%m/%d/%Y %I:%M:%S %p',
            filename='bag_creator.log',
            format='%(asctime)s %(message)s',
            level=logging.INFO)
        self.config = ConfigParser()
        self.config.read("local_settings.cfg")
        self.dest_location = self.config.get("Locations", "dest_location")
        # TODO: we should alias dart? where are we installing dart?
        self.as_client = ArchivesSpaceClient(baseurl=self.config.get(
            "ArchivesSpace", "baseurl"), username=self.config.get(
            "ArchivesSpace", "username"), password=self.config.get(
            "ArchivesSpace", "password"))
        self.dart_command = "we gotta figure this out"

    def run(self, top_dir, refid, rights_ids, files):
        """
        Args:
        refid (str)
        rights_ids (array)
        """
        # directory_to_bag = "some directory"
        self.refid = refid
        self.rights_ids = rights_ids
        self.files = files
        self.ao_uri = self.as_client.get_ao_uri(self.refid)
        ao_data = self.as_client.get_ao_data(self.ao_uri)
        dates = get_dates(ao_data)
        self.start_date, self.end_date = format_aspace_date(dates)
        # TODO: return path to created bag, any message from DART
        return self.refid

    def construct_job_params(self):
        job_params = {"workflowName": "Digitization Workflow"}
        job_params['packageName'] = "{}.tar".format(self.refid)
        job_params['files'] = self.files
        # TODO: get files in another method? to be passed into this method?
        job_params['files'] = ['/path/to/directory']
        tags = []
        tags.append(create_tag("ArchivesSpace-URI", self.ao_uri))
        tags.append(create_tag("Start-Date", self.start_date))
        tags.append(create_tag("End-Date", self.end_date))
        tags.append(create_tag("Origin", "digitization"))
        job_params['tags'] = tags
        return job_params

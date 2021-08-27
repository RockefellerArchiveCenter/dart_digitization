import json
from configparser import ConfigParser
from subprocess import PIPE, Popen

from .archivesspace import ArchivesSpaceClient
from .helpers import create_tag, format_aspace_date, get_dates


class BagCreator:

    def __init__(self):
        self.config = ConfigParser()
        self.config.read("local_settings.cfg")
        self.dest_location = self.config.get("Locations", "dest_location")
        # TODO: we should alias dart? where are we installing dart?
        self.dart_command = "we gotta figure this out"

    def run(self, top_dir, refid, rights_ids, files):
        """
        Args:
        refid (str)
        rights_ids (array)
        """
        # directory_to_bag = "some directory"
        self.as_client = ArchivesSpaceClient(baseurl=self.config.get(
            "ArchivesSpace", "baseurl"), username=self.config.get(
            "ArchivesSpace", "username"), password=self.config.get(
            "ArchivesSpace", "password"))
        self.refid = refid
        self.ao_uri = self.as_client.get_ao_uri(self.refid)
        ao_data = self.as_client.get_ao_data(self.ao_uri)
        dates = format_aspace_date(get_dates(ao_data))
        self.job_params = self.construct_job_params(rights_ids, files, dates)
        self.create_dart_job()
        # TODO: we'll probably want to return something else
        return self.refid

    def construct_job_params(self, rights_ids, files, dates):
        """Formats information for DART job parameters

        Args:
            rights_ids (array): list of rights ids
            files (array): list of full filepaths
            dates (tuple): begin and end dates

        Returns a dictionary"""
        job_params = {"workflowName": "Digitization Workflow"}
        job_params['packageName'] = "{}.tar".format(self.refid)
        job_params['files'] = files
        tags = []
        tags.append(create_tag("ArchivesSpace-URI", self.ao_uri))
        tags.append(create_tag("Start-Date", dates[0]))
        tags.append(create_tag("End-Date", dates[1]))
        tags.append(create_tag("Origin", "digitization"))
        for rights_id in rights_ids:
            tags.append(create_tag("Rights-ID", rights_id))
        job_params['tags'] = tags
        return job_params

    def create_dart_job(self):
        """Runs a DART job"""
        json_input = (json.dumps(self.job_params) + "\n").encode()
        cmd = "{} -- --stdin".format(self.dart_command)
        child = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
        stdout_data, stderr_data = child.communicate(json_input)
        if stdout_data is not None:
            raise Exception(stdout_data)
        elif stderr_data is not None:
            raise Exception(stderr_data)
        # TODO: will probably want to return path of created bag
        return child.returncode

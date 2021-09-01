import json
from configparser import ConfigParser
from subprocess import PIPE, Popen

from .archivesspace import ArchivesSpaceClient
from .helpers import create_tag, format_aspace_date, get_closest_dates


class BagCreator:

    def __init__(self):
        self.config = ConfigParser()
        self.config.read("local_settings.cfg")
        self.dart_command = self.config.get("DART", "dart")

    def run(self, refid, rights_ids, files):
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
        self.ao_uri = self.as_client.get_uri_from_refid(self.refid)
        ao_data = self.as_client.get_ao_data(self.ao_uri)
        begin_date, end_date = format_aspace_date(get_closest_dates(ao_data))
        self.job_params = self.construct_job_params(
            rights_ids, files, begin_date, end_date)
        self.create_dart_job()
        return self.refid

    def construct_job_params(self, rights_ids, files, begin_date, end_date):
        """Formats information for DART job parameters

        Args:
            rights_ids (array): list of rights ids
            files (array): list of full filepaths
            dates (tuple): begin and end dates

        Returns a dictionary"""

        job_params = {
            "workflowName": "Digitization Workflow",
            "packageName": "{}.tar".format(
                self.refid),
            "files": files}
        tags = []
        for tagname, uservalue in {"ArchivesSpace-URI": self.ao_uri,
                                   "Start-Date": begin_date, "End-Date": end_date, "Origin": "digitization"}.items():
            tags.append(create_tag(tagname, uservalue))
        for rights_id in rights_ids:
            tags.append(create_tag("Rights-ID", str(rights_id)))
        job_params['tags'] = tags
        return job_params

    def create_dart_job(self):
        """Runs a DART job"""
        json_input = (json.dumps(self.job_params) + "\n").encode()
        cmd = "{} -- --stdin".format(self.dart_command)
        child = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
        stdout_data, stderr_data = child.communicate(json_input)
        if child.returncode != 0:
            raise Exception(
                stdout_data.decode('utf-8'),
                stderr_data.decode('utf-8'))

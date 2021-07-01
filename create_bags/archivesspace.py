from asnake.aspace import ASpace


class ArchivesSpaceClient:
    def __init__(self, baseurl, username, password):
        self.client = ASpace(
            baseurl=baseurl,
            username=username,
            password=password).client

    def get_ao_uri(self):
        """Use find_by_refid endpoint to return the URI of an archival object"""
        pass

    def get_ao_data(self):
        """Gets data for an archival object, including ancestors"""
    pass

    def get_dates(self):
        """Returns begin and end dates in format YYYY-MM-DD. If date does not exist for an archival object, gets date information from nearest ancestor"""
    pass

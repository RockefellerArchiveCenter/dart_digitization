from asnake.aspace import ASpace

# from .helpers import get_dates


class ArchivesSpaceClient:
    def __init__(self, baseurl, username, password):
        self.client = ASpace(
            baseurl=baseurl,
            username=username,
            password=password).client

    def get_ao_uri(self, refid):
        """Use find_by_refid endpoint to return the URI of an archival object"""
        find_by_refid_url = "repositories/2/find_by_id/archival_objects?ref_id[]={}".format(
            refid)
        results = self.client.get(find_by_refid_url).json()
        return results['archival_objects'][0]['ref']

    def get_ao_data(self, ao_uri):
        """Gets data for an archival object, including ancestors"""
        ao_json = self.client.get(
            ao_uri, params={
                "resolve": ["ancestors"]}).json()
        return ao_json

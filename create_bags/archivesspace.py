from asnake.aspace import ASpace


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

    def get_dates(self, ao_json):
        if "dates" in ao_json.keys():
            dates = ao_json['dates'][0]
            begin_date = dates['begin']
            end_date = dates['end']
            return begin_date, end_date

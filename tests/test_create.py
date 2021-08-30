
from create_bags.bag_creator import BagCreator


def test_construct_job_params():
    bag_creator = BagCreator()
    bag_creator.refid = "jsdfjp90fsfjlk"
    bag_creator.ao_uri = "/whatever"
    rights_ids = [2, 4]
    dates = ("1940-01-01", "1940-06-01")
    files = ["/path/to/file1.tif", "/path/to/file2.tif"]
    job_params = bag_creator.construct_job_params(rights_ids, files, dates)
    assert isinstance(job_params, dict)
    for tag in job_params["tags"]:
        if tag["tagName"] == "Start-Date":
            assert tag["userValue"] == "1940-01-01"
    assert len(job_params["tags"]) == 6

# test run method

# test create_dart_job

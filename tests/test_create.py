import json
from os.path import join

import pytest
from create_bags.bag_creator import BagCreator
from create_bags.helpers import create_tag, format_aspace_date, get_dates


def test_construct_job_params():
    bag_creator = BagCreator()
    bag_creator.refid = "jsdfjp90fsfjlk"
    bag_creator.ao_uri = "/whatever"
    bag_creator.start_date = "1940-01-01"
    bag_creator.end_date = "1940-06-01"
    job_params = bag_creator.construct_job_params()
    assert isinstance(job_params, dict)
    for tag in job_params["tags"]:
        if tag["tagName"] == "Start-Date":
            assert tag["userValue"] == "1940-01-01"
    assert len(job_params["tags"]) == 4


def test_create_tag():
    created_tag = create_tag("testName", "test value")
    expected_result = {"tagFile": "bag-info.txt",
                       "tagName": "testName", "userValue": "test value"}
    assert created_tag == expected_result

# test_construct_job_params


def test_format_aspace_date(ao_date_data):
    dates = format_aspace_date(ao_date_data)
    assert dates[0] == "1950-01-01"
    assert dates[1] == "1969-12-31"


def test_get_dates(ao_data):
    date_data = get_dates(ao_data)
    assert isinstance(date_data, dict)


@pytest.fixture
def ao_data():
    path_to_file = join("tests", "data", "ao_data.json")
    with open(path_to_file, "r") as read_file:
        data = json.load(read_file)
    return(data)


@pytest.fixture
def ao_date_data():
    path_to_file = join("tests", "data", "ao_date_data.json")
    with open(path_to_file, "r") as read_file:
        data = json.load(read_file)
    return(data)

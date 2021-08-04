
from .helpers import create_tag


def test_create_tag():
    created_tag = create_tag("testName", "test value")
    expected_result = {"tagFile": "bag-info.txt",
                       "tagName": "testName", "userValue": "test value"}
    assert created_tag == expected_result

# test_construct_job_params

from pathlib import Path
from shutil import copytree

import pytest

# from create_bags.digitization_pipeline import DigitizationPipeline

# def test_run(tmp_path, special_projects_dir):
#     tmp_dir = tmp_path / "tmp"
#     tmp_dir.mkdir()
#     digitization_pipeline = DigitizationPipeline(tmp_dir, special_projects_dir)
#     assert digitization_pipeline.run([1, 2]) is True


@pytest.fixture
def tmp_dir(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("tmp_dir")
    return tmp_dir


@pytest.fixture
def special_projects_dir(tmp_path_factory):
    root_dir = tmp_path_factory.mktemp("root_dir")
    path_to_fixtures = Path(
        "tests",
        "data",
        "test-directories",
        "special_projects")
    copytree(path_to_fixtures, Path(root_dir, "special_projects"))
    special_projects_dir = Path(root_dir, "special_projects")
    return special_projects_dir

# @pytest.fixture(scope="session")
# def root_dir(tmp_path_factory):
#     img = compute_expensive_image()
#     fn = tmp_path_factory.mktemp("data") / "img.png"
#     img.save(fn)
#     return fn

# # contents of test_image.py
# def test_histogram(image_file):
#     img = load_image(image_file)
#     # compute and test histogram

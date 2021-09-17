# DART for Digitized Content

Uses [DART](https://github.com/APTrust/dart) to create bags of digitized content that will be sent to [Zorya](https://github.com/RockefellerArchiveCenter/zorya). 


## Requirements

The entire suite has the following system dependencies:
- Python 3 (tested on Python 3.7)
- ArchivesSnake (Python library) (0.9.1 or greater)
- [DART](https://github.com/APTrust/dart)

## Installation

*TBD*

## Configuration

This script requires a `local_settings.cfg` file. For an example of the sections and keys required, see [local_settings.cfg.example](local_settings.cfg.example) in this repository

### Configuring DART to work with this pipeline

This pipeline expects DART to have a workflow with the same name as defined in `local_settings.cfg`. The workflow should create a BagIt package, and should have a corresponding BagIt profile that expects the tags used in `BagCreator.construct_job_params`.

## Usage

*TBD*



## Tests

This library comes with unit tests. To quickly run tests, run `tox` from this directory.


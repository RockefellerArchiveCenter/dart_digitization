

def format_aspace_date(dates):
    '''
    Formats ASpace dates.

    Args:
        dates (dict): ArchivesSpace date JSON

    Returns:
        Tuple of a begin date and end date in format YYYY-MM-DD
    '''
    begin_date = dates['begin']
    end_date = False
    if dates['date_type'] == 'single':
        end_date = begin_date
    else:
        end_date = dates['end']
    if len(begin_date) == 4:
        begin_date = "{}-01-01".format(begin_date)
    if len(end_date) == 4:
        end_date = "{}-12-31".format(end_date)
    return begin_date, end_date


def get_dates(archival_object):
    '''
    Takes JSON for an archival object and returns a date from that object or its nearest ancestor with a date.

    Args:
        archival_object: JSON for AS archival object with resolved ancestors

    Returns:
        Dictionary for a date JSON
    '''
    # TODO: error handling
    dates = False
    if archival_object.get("dates"):
        dates = archival_object['dates'][0]
    else:
        for a in archival_object.get("ancestors"):
            if a.get("_resolved").get("dates"):
                dates = a['dates'][0]
                break
    return dates

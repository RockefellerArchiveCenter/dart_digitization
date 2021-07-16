

def format_aspace_date(date, date_type="end"):
    if date_type == "end":
        mm, dd = "12", "31"
    elif date_type == "begin":
        mm, dd = "01", "01"
    if len(date) == 4:
        return "{}-{}-{}".format(date, mm, dd)


def get_dates(archival_object):
    begin_date = False
    end_date = False
    if archival_object.get("dates"):
        dates = archival_object['dates'][0]
        begin_date = dates['begin']
        end_date = dates['end']
    else:
        for a in archival_object.get("ancestors"):
            if a.get("_resolved").get("dates"):
                dates = a['dates'][0]
                begin_date = dates['begin']
                end_date = dates['end']
    return begin_date, end_date

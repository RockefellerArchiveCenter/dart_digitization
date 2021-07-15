

def format_aspace_date(date, date_type="end"):
    if date_type == "end":
        mm, dd = "12", "31"
    elif date_type == "begin":
        mm, dd = "01", "01"
    if len(date) == 4:
        return "{}-{}-{}".format(date, mm, dd)

from datetime import date, datetime, timedelta


def clean_empty(d: (dict, list)):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (clean_empty(v) for v in d) if v]
    return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v}


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def current_utc_date():
    return datetime.utcnow().date()


def format_date_iso(date_value):
    if date is None:
        return None
    if isinstance(date_value, datetime):
        date_value = date_value.date()
    if isinstance(date_value, date):
        date_value = date_value.isoformat()
    return date_value


def format_datetime_iso(date_value):
    if date is None:
        return None
    if isinstance(date_value, date):
        date_value = datetime(date_value.year, date_value.month, date_value.day)
    if isinstance(date_value, datetime):
        date_value = date_value.isoformat()
    return date_value

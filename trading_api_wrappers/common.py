from datetime import date, datetime, timedelta
from urllib.parse import urlencode

# local
from . import logger


def check_keys(key, secret):
    if not key or not secret:
        msg = 'API Key and Secret are needed!'
        logger.log_error(msg)
        raise ValueError(msg)


def build_parameters(parameters):
    if parameters:
        p = clean_parameters(parameters)
        return urlencode(p, True)
    else:
        return None


def build_route(path, params=None):
    built_params = build_parameters(params)
    if built_params:
        return f'{path}?{built_params}'
    else:
        return path


def clean_parameters(parameters: dict):
    return {k: v for k, v in parameters.items() if v is not None}


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
        date_value = datetime(
            date_value.year, date_value.month, date_value.day)
    if isinstance(date_value, datetime):
        date_value = date_value.isoformat()
    return date_value

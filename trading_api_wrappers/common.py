import time
from datetime import datetime, timedelta
from urllib.parse import urlencode

# local
from . import logger


def gen_nonce():
    # Sleeps 200ms to avoid flooding the server with requests.
    time.sleep(0.2)
    # Get a str from the current time in microseconds.
    return str(int(time.time() * 1E6))


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
        return '{0:s}?{1:s}'.format(path, built_params)
    else:
        return path


def clean_parameters(parameters: dict):
    if parameters:
        return {k: v for k, v in parameters.items() if v is not None}


def update_dictionary(old_dict: dict, new_dict: dict):
    if new_dict:
        keys = list(new_dict.keys())
        for k in keys:
            old_dict[k] = new_dict[k]


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def current_utc_date():
    return datetime.utcnow().date()

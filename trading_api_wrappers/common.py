from urllib.parse import urlencode
import logging
import time
# pip
import requests


def gen_nonce():
    # Sleeps 200ms to avoid flooding the server with requests.
    time.sleep(0.2)
    # Get a str from the current time in microseconds.
    return str(int(time.time() * 1E6))


def log_message(msg):
    msg = "Trading API: " + msg
    return msg


def log_error(msg):
    logging.error(log_message(msg))
    return log_message(msg)


def log_warning(msg):
    logging.warning(log_message(msg))
    return log_message(msg)


def log_request_exception(err: requests.RequestException):
    msg = 'RequestsException: ' + str(err)
    return log_error(msg)


def log_json_decode():
    msg = 'JSONDecodeError: Unable to decode JSON from response (no content).'
    return log_error(msg)


def check_keys(key, secret):
    if not key or not secret:
        msg = 'API Key and Secret are needed!'
        log_error(msg)
        raise ValueError(msg)


def check_response(response):
    if 'message' in response:
        msg = 'ResponseMessage: ' + response['message']
        log_error(msg)
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

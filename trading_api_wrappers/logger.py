import logging


def log_message(msg):
    msg = "Trading API: " + msg
    return msg


def log_error(msg):
    logging.error(log_message(msg))
    return log_message(msg)


def log_exception(e, msg):
    logging.exception(log_message(msg))
    log_message(msg)


def log_warning(msg):
    logging.warning(log_message(msg))
    return log_message(msg)

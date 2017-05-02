from . import logger


class Error(Exception):
    pass


class Unavailable(Error):
    pass


class TradingAPIError(Error):
    def __init__(self, message):
        self.message = message
        logger.log_error(self.message)


class InvalidResponse(TradingAPIError):
    def __init__(self, response):
        msg = ('InvalidResponse (Code: {r.status_code}): '
               'Message: {r.text} ({r.url})'.
               format(r=response))
        super(InvalidResponse, self).__init__(msg)


class DecodeError(TradingAPIError):
    def __init__(self):
        msg = 'DecodeError: Unable to decode JSON from response (no content).'
        super(DecodeError, self).__init__(msg)

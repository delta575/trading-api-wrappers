from requests import Response

from requests.exceptions import RequestException


class APIException(RequestException):
    pass


class InvalidResponse(APIException):
    def __init__(self, error_msg: str, r: Response):
        # Add status code
        message = str(r.status_code)
        # Check for client or server errors
        if 400 <= r.status_code < 500:
            message = f"{message} Client Error:"
        elif 500 <= r.status_code < 600:
            message = f"{message} Server Error:"
        # Add reason
        message = f"{message} {r.reason}"
        # Add message from source
        if error_msg:
            message = f"{message} ({error_msg})"
        # Add url
        message = f"{message} for url: {r.url}"

        super().__init__(message, response=r)
        self.message = message


class DecodeError(APIException):
    def __init__(self, msg, r: Response):
        super().__init__(msg, response=r)

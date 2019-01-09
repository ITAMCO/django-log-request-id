import logging
from log_request_id import local, NO_REQUEST_ID


class RequestIDFilter(logging.Filter):

    def filter(self, record):
        if not hasattr(record, 'request_id'):
            record.request_id = getattr(local, 'request_id', NO_REQUEST_ID)
        return True

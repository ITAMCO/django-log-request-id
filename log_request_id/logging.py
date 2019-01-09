import logging

__REQUEST_CLASSES = []

try:
    from django.http import HttpRequest

    __REQUEST_CLASSES.append(HttpRequest)
except:
    pass

try:
    from rest_framework.request import Request

    __REQUEST_CLASSES.append(Request)
except:
    pass

REQUEST_CLASSES = tuple(__REQUEST_CLASSES)


class Logger:
    def __init__(self, logger):
        self.logger = logger

    def __getattr__(self, name):
        def method(*args, **kwargs):
            args = list(args)

            request_id = None

            # If request is first arg, grab id there
            if isinstance(args[0], REQUEST_CLASSES):
                request_id = args[0].id
                del args[0]

            # If request is a kwarg, grab id there
            if 'request' in kwargs:
                request_id = kwargs['request'].id
                del kwargs['request']

            # If any arg is a request, grab id there
            if request_id is None:
                for arg in args:
                    if isinstance(arg, REQUEST_CLASSES):
                        request_id = arg.id
                        arg.remove(arg)
                        break

            # If any kwarg is a request, grab id there
            if request_id is None:
                for key, value in kwargs.items():
                    if isinstance(value, REQUEST_CLASSES):
                        request_id = value.id
                        del kwargs[key]
                        break

            # If there was a request ID, add it to extras
            if request_id is not None:
                if 'extra' not in kwargs:
                    kwargs['extra'] = {}
                kwargs['extra']['request_id'] = request_id

            return getattr(self.logger, name)(*tuple(args), **kwargs)
        return method


def getLogger(name=None):
    return Logger(logging.getLogger(name))

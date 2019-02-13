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

            request = None

            # If request is first arg, grab id there
            if isinstance(args[0], REQUEST_CLASSES):
                request = args[0]
                del args[0]

            # If request is a kwarg, grab id there
            if 'request' in kwargs:
                request = kwargs['request']
                del kwargs['request']

            # If any arg is a request, grab id there
            if request is None:
                for arg in args:
                    if isinstance(arg, REQUEST_CLASSES):
                        request = arg
                        arg.remove(arg)
                        break

            # If any kwarg is a request, grab id there
            if request is None:
                for key, value in kwargs.items():
                    if isinstance(value, REQUEST_CLASSES):
                        request = value
                        del kwargs[key]
                        break

            # If there was a request ID, add it to extras
            if request is not None:
                if 'extra' not in kwargs:
                    kwargs['extra'] = {}

                if hasattr(request, 'id'):
                    kwargs['extra']['request_id'] = request.id

                if hasattr(request, 'method'):
                    kwargs['extra']['method'] = request.method

                if hasattr(request, 'path'):
                    kwargs['extra']['path'] = request.path

                if hasattr(request, 'status_code'):
                    kwargs['extra']['status_code'] = request.status_code

                if hasattr(request, 'user'):
                    if hasattr(request.user, 'id'):
                        kwargs['extra']['user'] = request.user.id

            return getattr(self.logger, name)(*tuple(args), **kwargs)
        return method


def getLogger(name=None):
    return Logger(logging.getLogger(name))

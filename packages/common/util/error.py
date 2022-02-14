from ..domain import constants

FAIL = 'fail'
OK = 'ok'

def exception_urn(instance):
    return "{urn_base}:error:{inst}".format(urn_base=constants.SERVICE_URN_BASE, inst=instance)

class ServiceError(Exception):
    """
    Base Error Class for service errors
    """

    def __init__(self, message="", name="", ctx={}, code=500, klass="", retryable=False):
        self.code = 500 if code is None else code
        self.retryable = retryable
        self.message = message
        self.name = name
        self.ctx = ctx
        self.klass = klass
        super().__init__(self.message)

    def error(self):
        return {'error': self.message, 'code': self.code, 'step': self.name, 'ctx': self.ctx}

    def duplicate_error(self):
        return "Duplicate" in self.message

class DynamoError(ServiceError):
    def not_found(cls):
        return "DoesNotExist" in cls.klass

class UnExpectedServiceException(ServiceError):
    pass

class UnmetExpectation(ServiceError):
    pass


class DuplicateEventError(ServiceError):
    pass

class EnvironmentNotSetup(ServiceError):
    pass
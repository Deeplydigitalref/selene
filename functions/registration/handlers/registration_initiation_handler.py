import uuid
from typing import Dict
from pymonad.tools import curry

from pyfuncify import fn, monad, logger, chronos

from common.util import error

_CTX = {}

instrumentables = []

class AggregateError(error.ServiceError):
    pass

def handle(request: Dict) -> monad.MEither:
    _CTX['tracer'] = request.tracer

    return monad.Right(None)

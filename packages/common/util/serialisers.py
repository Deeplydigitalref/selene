from pyfuncify.app import Serialiser
from ..domain import webauthn_helpers

class WebAuthnRegistrationSerialiser(Serialiser):
    def __init__(self, serialisable, serialisaton=None):
        self.serialisable = serialisable
        self.serialisation = serialisaton

    def serialise(self):
        return webauthn_helpers.serialise_options(self.serialisable.registration_options)


class WebAuthnRegistrationCompletionSerialiser(Serialiser):
    def __init__(self, serialisable, serialisaton=None):
        self.serialisable = serialisable
        self.serialisation = serialisaton

    def serialise(self):
        return '{}'

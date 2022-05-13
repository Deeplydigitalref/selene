from typing import Tuple

from common.domain.subject import registration
from key_management.domain import sym_enc



def internal_client() -> Tuple:
    service_value = {
        'serviceName': 'urn:service:service1',
        'realm': 'https://example.com/ontology/sec/realm/internal'
    }
    client = registration.new_service(service_value)
    secret = sym_enc.jwe_decrypt(client.client_secret)
    return client, secret, None

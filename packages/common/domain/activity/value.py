from enum import Enum
from attrs import define, field

from common.domain.subject import value as sub
from common.repository.activity import activity as repo

class ActivityRecommendation(Enum):
    VALIDATION_ERROR = 'urn:idp:recommendation:returnValuationError'

class ActivityError(Enum):
    CLIENT_NOT_SUPPORTED = 'urn:idp:error:activitiesRegistrationNotSupported'

@define
class Activity:
    uuid: str
    service_urn: str
    label: str
    activity: str
    definition: str
    policy_statements: dict
    client_uuid: str = field(default=None)
    client: sub.Subject = field(default=None)
    model: repo.ActivityModel = field(default=None)

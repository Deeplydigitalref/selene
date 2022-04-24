from typing import Type

from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, MapAttribute, ListAttribute, UTCDateTimeAttribute, DiscriminatorAttribute, JSONAttribute
)

from common.util.env import Env

class BaseModel(Model):
    """
    Base Model consisting of the single table convention; the hash and range keys named PK and SK respectively.
    """
    class Meta:#(Model.Meta):
        table_name = Env.dynamodb_table()
        region = Env.region_name
        # write_capacity_units = 10
        # read_capacity_units = 10
    PK = UnicodeAttribute(hash_key=True)
    SK = UnicodeAttribute(range_key=True)
    kind = DiscriminatorAttribute()

class WebAuthnSubjectRegistration(BaseModel, discriminator='auth:subject:webAuthnRegistration'):
    reg_uuid = UnicodeAttribute()
    subject_name = UnicodeAttribute()
    sub = UnicodeAttribute(null=True)
    state = UnicodeAttribute()
    encoded_challenge = UnicodeAttribute()
    credential = JSONAttribute(null=True)

class Subject(BaseModel, discriminator='auth:subject:subject'):
    sub = UnicodeAttribute()
    subject_name = UnicodeAttribute()
    state = UnicodeAttribute()
    registrations = ListAttribute()


class Circuit(BaseModel, discriminator='auth:circuit'):
    circuit_state = UnicodeAttribute(null=True)
    last_state_chg_time = UTCDateTimeAttribute(null=True)
    failures = NumberAttribute(null=True)

class Cache(BaseModel, discriminator='auth:cache'):
    value = UnicodeAttribute()

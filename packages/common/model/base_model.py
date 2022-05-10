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

class CredentialRegistration(BaseModel, discriminator='auth:subject:credentialRegistration'):
    reg_uuid = UnicodeAttribute()
    subject_name = UnicodeAttribute()
    state = UnicodeAttribute()
    realm = UnicodeAttribute()
    is_class_of = UnicodeAttribute()
    sub = UnicodeAttribute(null=True)
    encoded_challenge = UnicodeAttribute(null=True)
    client_secret = UnicodeAttribute(null=True)
    credential = JSONAttribute(null=True)


class Subject(BaseModel, discriminator='auth:subject:subject'):
    sub = UnicodeAttribute()
    is_class_of = UnicodeAttribute()
    subject_name = UnicodeAttribute()
    state = UnicodeAttribute()
    registrations = ListAttribute()

class Authorisation(BaseModel, discriminator='auth:subject:authorisation'):
    exp = NumberAttribute()
    state = UnicodeAttribute()
    is_class_of = UnicodeAttribute()
    sub = UnicodeAttribute()


class ActivityGroup(BaseModel, discriminator='auth:activity:activityGroup'):
    display_name = UnicodeAttribute()
    label = UnicodeAttribute()

class Activity(BaseModel, discriminator='auth:activity:activity'):
    display_name = UnicodeAttribute()
    label = UnicodeAttribute()


class Circuit(BaseModel, discriminator='auth:circuit'):
    circuit_state = UnicodeAttribute(null=True)
    last_state_chg_time = UTCDateTimeAttribute(null=True)
    failures = NumberAttribute(null=True)

class Cache(BaseModel, discriminator='auth:cache'):
    value = UnicodeAttribute()

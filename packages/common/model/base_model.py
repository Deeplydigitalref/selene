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
    uuid = UnicodeAttribute()
    exp = NumberAttribute()
    state = UnicodeAttribute()
    is_class_of = UnicodeAttribute()
    sub = UnicodeAttribute()
    azp = UnicodeAttribute()
    jwt = UnicodeAttribute()


class ActivityGroup(BaseModel, discriminator='auth:activity:activityGroup'):
    uuid = UnicodeAttribute()
    asserted_client = UnicodeAttribute()
    label = UnicodeAttribute()
    activity_group = UnicodeAttribute()
    definition = UnicodeAttribute()
    policy_statements = ListAttribute()

class Activity(BaseModel, discriminator='auth:activity:activity'):
    uuid = UnicodeAttribute()
    service_urn = UnicodeAttribute()
    label = UnicodeAttribute()
    activity = UnicodeAttribute()
    definition = UnicodeAttribute()
    policy_statements = ListAttribute()
    client_uuid = UnicodeAttribute()

class Circuit(BaseModel, discriminator='auth:circuit'):
    circuit_state = UnicodeAttribute(null=True)
    last_state_chg_time = UTCDateTimeAttribute(null=True)
    failures = NumberAttribute(null=True)

class Cache(BaseModel, discriminator='auth:cache'):
    value = UnicodeAttribute()


def scan():
    """
    For testing only
    :return:
    """
    return [b.attribute_values for b in BaseModel.scan()]

def p():
    models = scan()
    [print("{}\n".format(model)) for model in models]
    pass
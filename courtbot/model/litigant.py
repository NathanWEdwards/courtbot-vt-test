from json import load
from logging import getLogger

from mongoengine import EmbeddedDocument
from mongoengine import EmbeddedDocumentField
from mongoengine import StringField

from courtbot.model.role import Role
from courtbot.utils.utils import json_choice


class Litigant(EmbeddedDocument):
    entity_id = StringField(required=True)
    last_name = StringField(required=True)
    first_name = StringField(required=True)
    full_name = StringField(required=True)
    role = EmbeddedDocumentField(Role, required=True)
    number = StringField(required=True)


def litigant_document(json_object):
    litigant = json_choice(json_object)
    role = Role(
        code=litigant["role"]["code"],
        rank=litigant["role"]["rank"],
        description=litigant["role"]["description"],
    )
    litigant_document = Litigant(
        entity_id=litigant["entity_id"],
        last_name=litigant["last_name"],
        first_name=litigant["first_name"],
        full_name=litigant["full_name"],
        role=role,
        number=litigant["number"],
    )
    return litigant_document

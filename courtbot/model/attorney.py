from json import load
from logging import getLogger

from mongoengine import EmbeddedDocument
from mongoengine import StringField
from courtbot.utils.utils import json_choice


class Attorney(EmbeddedDocument):
    entity_id = StringField(required=True)
    last_name = StringField(required=True)
    first_name = StringField(required=True)
    suffix = StringField(required=True)
    full_name = StringField(required=True)


def attorney_document(json_object):
    attorney = json_choice(json_object)
    attorney_document = Attorney(
        entity_id=attorney["entity_id"],
        last_name=attorney["last_name"],
        first_name=attorney["first_name"],
        suffix=attorney["suffix"],
        full_name=attorney["full_name"],
    )
    return attorney_document

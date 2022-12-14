from mongoengine import EmbeddedDocument
from mongoengine import StringField

from courtbot.utils.utils import randstring
from courtbot.utils.utils import json_choice


class Case(EmbeddedDocument):
    name = StringField(required=True)
    status = StringField(required=True)
    type = StringField(required=True)


def case_document(json_object):
    """
    Mocks a case document.

    :return: {str} A case name
    """
    case = json_choice(json_object)
    case_document = Case(name=case["name"], status=case["status"], type=case["type"])
    return case_document

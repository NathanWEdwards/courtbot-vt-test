from mongoengine import EmbeddedDocument
from mongoengine import StringField
from courtbot.utils.utils import json_choice


class Judge(EmbeddedDocument):
    code = StringField(required=True)
    name = StringField(required=True)


def judge_document(json_object):
    judge = json_choice(json_object)
    judge_document = Judge(code=judge["code"], name=judge["name"])
    return judge_document

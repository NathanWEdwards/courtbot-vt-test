from mongoengine import EmbeddedDocument
from mongoengine import StringField


class Role(EmbeddedDocument):
    code = StringField(required=True)
    rank = StringField(required=True)
    description = StringField(required=True)

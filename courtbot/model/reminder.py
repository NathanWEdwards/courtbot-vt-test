from mongoengine import BooleanField
from mongoengine import Document
from mongoengine import StringField

class Reminder(Document):
    id = StringField(primary_key=True, required=True)
    number = StringField(required=True)
    phone = StringField(required=True)
    active = BooleanField(required=True, default=True)
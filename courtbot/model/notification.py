from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import StringField

class Notification(Document):
    id = StringField(primary_key=True, required=True)
    number = StringField(required=True)
    phone = StringField(required=True)
    event_date = DateTimeField(required=True)
    error = StringField()
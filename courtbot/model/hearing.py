from datetime import datetime
from datetime import timedelta
from mongoengine import EmbeddedDocument
from mongoengine import StringField

from courtbot.utils.utils import randdate
from courtbot.utils.utils import randstring


class Hearing(EmbeddedDocument):
    date = StringField(required=True)
    start_time = StringField(required=True)
    type_code = StringField(required=True)
    type = StringField(required=True)


def hearing_date_field_format_value(date):
    """
    Format a datetime object to the expected formatting.

    :return: {str} A formatted string representation of a hearing date.
    """
    return date.strftime("%m/%d/%Y")


def hearing_start_time_field_format_value(date):
    """
    Format a datetime object to the expected formatting.

    :return: {str} A formatted string representation of a hearing start time.
    """
    return date.strftime("%H:%M")


def hearing_date_field_value():
    """
    Mocks a hearing date.

    :return: {str} A datetime object formatted as a string.
    """
    date = randdate.strptime("%m/%d/%Y %H:%M")
    return date.strftime("%m/%d/%Y")


def hearing_start_time_field_value():
    """
    Mocks a hearing start time.

    :return: {str} A datetime object formatted as a string.
    """
    date = randdate.strptime("%m/%d/%Y %H:%M")
    return date.strftime("%H:%M")


def hearing_type_code_field_value():
    """
    Mocks a hearing type code field value.

    :return: {str} A hearing type code as a string.
    """
    return randstring()


def hearing_type_field_value():
    """
    Mocks a hearing type field value.

    :return: {str} A hearing type as a string.
    """
    return randstring()


def hearing_document(
    date_of_hearing=None, hearing_type_code=None, hearing_type=None
):

    if date_of_hearing is None:
        date_of_hearing = randdate()

    date = hearing_date_field_format_value(date_of_hearing)
    start_time = hearing_start_time_field_format_value(date_of_hearing)

    if hearing_type_code is None:
        hearing_type_code = hearing_type_code_field_value()

    if hearing_type is None:
        hearing_type = hearing_type_field_value()

    hearing_document = Hearing(
        date=date, start_time=start_time, type_code=hearing_type_code, type=hearing_type
    )
    return hearing_document

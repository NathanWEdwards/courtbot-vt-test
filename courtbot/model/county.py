from mongoengine import EmbeddedDocument
from mongoengine import StringField

from courtbot.utils.utils import randstring


class County(EmbeddedDocument):
    code = StringField(required=True)
    name = StringField(required=True)


def county_code_field_value():
    """
    Mocks a county code.

    :return: {str} A county code
    """

    return randstring()


def county_name_field_value():
    """
    Mocks a county name.

    :return: {str} A county name
    """
    return "%s County" % (randstring())


def county_document():
    """
    Provides an embedded document county document with county name and county code values set by calls made to corresponding mock methods.
    """
    county_code = county_code_field_value()
    county_name = county_name_field_value()
    county_document = County(code=county_code, name=county_name)
    return county_document

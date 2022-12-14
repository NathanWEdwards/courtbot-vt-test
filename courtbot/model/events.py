from random import choice
from random import randint
from string import ascii_uppercase

from mongoengine import EmbeddedDocumentField
from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import StringField
from courtbot.model.attorney import Attorney
from courtbot.model.attorney import attorney_document
from courtbot.model.case import Case
from courtbot.model.case import case_document
from courtbot.model.county import County
from courtbot.model.county import county_document
from courtbot.model.court_division import court_division_field_value
from courtbot.model.hearing import Hearing
from courtbot.model.hearing import hearing_document
from courtbot.model.judge import Judge
from courtbot.model.judge import judge_document
from courtbot.model.litigant import Litigant
from courtbot.model.litigant import litigant_document
from courtbot.utils.utils import randdate
from courtbot.utils.utils import randstring
from courtbot.utils.utils import json_choice


class Event(Document):
    id = StringField(primary_key=True, required=True)
    date = DateTimeField(required=True)
    county = EmbeddedDocumentField(County, required=True)
    division = StringField(required=True)
    judge = EmbeddedDocumentField(Judge, required=True)
    court_room_code = StringField(required=True)
    hearing = EmbeddedDocumentField(Hearing, required=True)
    docket_id = StringField(required=True)
    docket_number = StringField(required=True)
    case = EmbeddedDocumentField(Case, required=True)
    litigant = EmbeddedDocumentField(Litigant, required=True)
    attorney = EmbeddedDocumentField(Attorney, required=True)
    calendar_id = StringField(required=True)


# Methods that mock document field values.


def calendar_id_field_value():
    """
    Mocks a calendar id field value for the 'events' object relational mapping.
    :return: {str} A calendar id value
    """
    return str(randint(1, 365))


def court_room_code_field_value():
    """
    Creates a court room code.
    :return: {str} The code designated for a court room
    """
    return randstring()


def event_date_field_value():
    """
    Provides a date in the future.
    :return: {str} A date and time as strings
    """
    return randdate().strftime("%m/%d/%Y %H:%M")


def docket_number_field_value(code=None, case_type=None):
    """
    Provides a string representing a docket number.
    :param code: {str} A docket identifier string
    :param case_type: {str} A case type abbreviation
    :return: {str} A docket number
    """
    if code is None:
        code = choice(ascii_uppercase)
    if case_type is None:
        case_type = str(randint(1, 200))

    return "%02d-%s-%02d" % (randint(1, 200), case_type, randint(1, 200))


def docket_id_field_value(docket_number=None, court_code=None):
    """
    Returns a docket identifier with a docket identifier and county code.
    :return: {str} A docket identifier
    """
    if docket_number is None:
        docket_number = docket_number_field_value()
    if court_code is None:
        court_code = randstring()
    docket_id = " ".join([docket_number, court_code])

    return docket_id


def event_document(attorneys, cases, court_divisions, judges, litigants, docket_ids=None):
    """
    Mocks an event document.

    :attorneys:
    :cases:
    :court_division:
    :judges:
    :litigants:
    """
    event_date = event_date_field_value()
    county_embedded_document = county_document()
    division = court_division_field_value(court_divisions)
    judge_embedded_document = judge_document(judges)
    court_room_code = court_room_code_field_value()
    hearing_embedded_document = hearing_document()
    docket_number=None
    docket_id=None
    if docket_ids is None:
        docket_number = docket_number_field_value()
        docket_id = docket_id_field_value(
            docket_number=docket_number, court_code=division
        )
    else:
        docket_id = json_choice(docket_ids)
        docket_number = (docket_id.split(" "))[0]
    case_embedded_document = case_document(cases)
    litigant_embedded_document = litigant_document(litigants)
    attorney_embedded_document = attorney_document(attorneys)
    calendar_id = calendar_id_field_value()
    event_id = "%s-%s-%s-%s-%s" % (
        county_embedded_document["code"],
        division,
        docket_number,
        litigant_embedded_document["entity_id"],
        litigant_embedded_document["role"]["code"],
    )
    event_document = Event(
        id=event_id,
        date=event_date,
        county=county_embedded_document,
        division=division,
        judge=judge_embedded_document,
        court_room_code=court_room_code,
        hearing=hearing_embedded_document,
        docket_number=docket_number,
        docket_id=docket_id,
        case=case_embedded_document,
        litigant=litigant_embedded_document,
        attorney=attorney_embedded_document,
        calendar_id=calendar_id,
    )
    return event_document


def event_document_as_court_schedule_file_row(event_document):
    row = [
        "column_0_not_implemented",
        event_document.county.code,
        event_document.hearing.date,
        event_document.division,
        event_document.judge.code,
        event_document.hearing.start_time,
        "column_6_not_implemented",
        event_document.court_room_code,
        event_document.hearing.type_code,
        event_document.docket_id,
        event_document.docket_number,
        event_document.case.name,
        event_document.litigant.entity_id,
        event_document.litigant.last_name,
        event_document.litigant.first_name,
        event_document.litigant.full_name,
        event_document.litigant.role.code,
        event_document.litigant.role.rank,
        event_document.litigant.number,
        event_document.attorney.entity_id,
        event_document.attorney.last_name,
        event_document.attorney.first_name,
        event_document.attorney.suffix,
        event_document.attorney.full_name,
        event_document.county.name,
        event_document.hearing.type,
        event_document.case.type,
        event_document.case.status,
        event_document.judge.name,
        event_document.litigant.role.description,
        event_document.calendar_id,
    ]
    return row
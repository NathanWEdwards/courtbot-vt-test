from datetime import datetime
from datetime import timedelta
from json import load
from pathlib import Path
from logging import getLogger
from random import choice
from random import randint
from string import ascii_uppercase
from string import ascii_lowercase

def json_choice(_json_object):
    """
    Select an element at random from a JSON array.

    :param _json_object: {str|list}
    """
    json_object = None
    if isinstance(_json_object, str) or isinstance(_json_object, Path):
        try:
            with open(_json_object, "r") as resource:
                json_objects = load(resource)
                json_object = choice(json_objects)
            return json_object
        except Exception as e:
            log = getLogger("pytest")
            log.error(e)
    else:
        json_object = choice(_json_object)
    return json_object

def randphonenumber():
    """
    This method returns a random 10-digit phone number string.

    :return: {str} A phone number.
    """
    area_code = randint(1,999)
    exchange_code = randint(1,999)
    line_number = randint(1,9999)

    return "(%03d) %03d-%04d" % (area_code, exchange_code, line_number)


def randstring():
    """
    This method provides a random ASCII string.

    :return: {str} An ASCII string
    """
    string = choice(ascii_uppercase)
    string += "".join(choice(ascii_lowercase) for _ in range(randint(3, 10)))

    return string


def randdate():
    """
    This method returns a datetime object with a date set in the future.

    :return: {datetime} A datetime object.
    """
    current_time = datetime.now()
    days_to_offset = randint(2, 365)
    hours_to_offset = randint(9, 16)
    delta = timedelta(days=days_to_offset)
    generated_date = current_time + delta
    generated_date = generated_date.replace(hour=hours_to_offset, minute=0, second=0)
    # If the day falls on a weekend then set the day to a weekday
    day_of_week = generated_date.weekday()
    if day_of_week > 4:
        days_to_offset = randint(2, 5)
        delta = timedelta(days=days_to_offset)
        generated_date = generated_date + delta
    return generated_date
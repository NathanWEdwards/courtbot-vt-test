from json import load
from logging import getLogger
from courtbot.utils.utils import json_choice


def court_division_field_value(json_object):
    court_division = json_choice(json_object)
    return court_division

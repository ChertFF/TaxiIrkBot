import logging

from aiogram import types
from time import gmtime, strftime

from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import emoji

from data import config

from utils.db_api import quick_commands


def check_time_second():
    time = int(strftime("%H", gmtime()))
    if 12 <= time <= 23 and time >= 3:
        return False
    else:
        return True

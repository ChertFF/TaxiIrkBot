import logging

from aiogram import types
from time import gmtime, strftime
from datetime import datetime, timedelta
import datetime

from aiogram.utils import emoji

from data import config

from utils.db_api import quick_commands


def check_time():
    current_time = datetime.datetime.now().time()
    start_time = datetime.time(3, 0)
    end_time = datetime.time(18, 0)
    if start_time <= end_time:
        return start_time <= current_time <= end_time
    else:
        return start_time <= current_time or current_time <= end_time

def second_check_time():
    current_time = datetime.datetime.now().time()
    start_time = datetime.time(3, 0)
    end_time = datetime.time(18, 0)
    if start_time <= end_time:
        return start_time <= current_time <= end_time
    else:
        return start_time <= current_time or current_time <= end_time
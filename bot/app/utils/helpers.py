from datetime import datetime as dt


def num_to_weekday(num: int):
    """Converts weekday number to its name"""

    return dt(2023, 1, num).strftime('%A')


def str_today():
    """Returns today's weekday"""

    return num_to_weekday(dt.today().weekday())


def normalize_day_offset(offset):
    """
    Normalize the day offset to a value within
    the 0-6 range (representing days of the week).
    """

    return (offset % 7 + 7) % 7

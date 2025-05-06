from datetime import date, timedelta


def get_start_date():
    return date.today() + timedelta(days=1)


def get_end_date():
    return date.today() + timedelta(days=15)

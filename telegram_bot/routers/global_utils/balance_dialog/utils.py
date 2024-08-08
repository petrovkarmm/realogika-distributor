from datetime import datetime


def convert_datetime(iso_date_str):
    date_object = datetime.fromisoformat(iso_date_str)
    formatted_datetime = date_object.strftime('%d.%m.%Y %H:%M:%S')

    return formatted_datetime

from datetime import datetime
from dateutil.relativedelta import relativedelta

time_format = "%m/%d/%Y %H:%M:%S"


class Time:
    @staticmethod
    def format_date(date):
        return date.strftime(time_format) if date else None

    @staticmethod
    def format_date_by_year(date):
        return date.strftime("%Y/%m/%d %H:%M:%S")

    @staticmethod
    def today():
        return Time.format_date(datetime.today())

    @staticmethod
    def today_iso():
        return datetime.isoformat(datetime.today())

    @staticmethod
    def one_year_from_now():
        return Time.format_date(datetime.today() + relativedelta(years=1))

    @staticmethod
    def one_year_from_now_iso():
        return datetime.isoformat(datetime.today() + relativedelta(year=1))

    @staticmethod
    def yesterday():
        return Time.format_date(datetime.today() - relativedelta(days=1))

    @staticmethod
    def yesterday_iso():
        return datetime.isoformat(datetime.today() - relativedelta(days=1))

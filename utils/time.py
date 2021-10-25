from datetime import datetime
from dateutil.relativedelta import relativedelta

time_format = "%m/%d/%Y %H:%M:%S"
iso_format = "%Y-%m-%dT%H:%M:%S.%fZ"


class Time:
    @staticmethod
    def format_date(date):
        return date.strftime(time_format) if date else None

    @staticmethod
    def to_iso(date):
        return date.strftime(iso_format)

    @staticmethod
    def format_date_by_year(date):
        return date.strftime("%Y/%m/%d %H:%M:%S")

    @staticmethod
    def today():
        return Time.format_date(datetime.today())

    @staticmethod
    def today_iso():
        return Time.to_iso(datetime.today())

    @staticmethod
    def one_year_from_now():
        return Time.format_date(Time._one_year())

    @staticmethod
    def one_year_from_now_iso():
        return Time.to_iso(Time._one_year())

    @staticmethod
    def yesterday():
        return Time.format_date(Time._yesterday())

    @staticmethod
    def yesterday_iso():
        return Time.to_iso(Time._yesterday())

    @staticmethod
    def _yesterday():
        return datetime.today() - relativedelta(days=1)

    @staticmethod
    def _one_year():
        return datetime.today() + relativedelta(years=1)


class TimeStamp:
    @staticmethod
    def now():
        return datetime.utcnow().__str__()

    @staticmethod
    def days_ago(num):
        return (datetime.utcnow() - relativedelta(days=num)).__str__()

    @staticmethod
    def weeks_ago(num):
        return (datetime.utcnow() - relativedelta(weeks=num)).__str__()


class Date:
    @staticmethod
    def today():
        return datetime.utcnow().date()

    @staticmethod
    def days_ago(num):
        return datetime.utcnow().date() - relativedelta(days=num)

    @staticmethod
    def weeks_ago(num):
        return datetime.utcnow().date() - relativedelta(weeks=num)

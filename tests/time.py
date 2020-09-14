from datetime import datetime
from dateutil.relativedelta import relativedelta


class Time:
    @staticmethod
    def format_date(date):
        return date.strftime("%m/%d/%Y %H:%M:%S")

    @staticmethod
    def today():
        return Time.format_date(datetime.today())

    @staticmethod
    def one_year_from_now():
        return Time.format_date(datetime.today() + relativedelta(years=1))

    @staticmethod
    def yesterday():
      return Time.format_date(datetime.today() - relativedelta(days=1))

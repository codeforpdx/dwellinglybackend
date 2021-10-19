import re


def blank(value):
    return re.match(r"\A\s*\Z", value)

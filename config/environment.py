import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Default(object):
    # config DataBase
    SECRET_KEY = os.environ.get("SECRET_KEY")
    WORK_FACTOR = 12
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_AUTH_USERNAME_KEY = os.environ.get("JWT_AUTH_USERNAME_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get("JWT_ACCESS_TOKEN_EXPIRES")
    JWT_REFRESH_TOKEN_EXPIRES = os.environ.get("JWT_REFRESH_TOKEN_EXPIRES")

    # configure mail server
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = os.environ.get("MAIL_PORT", 465)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", False)
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", True)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    # Configure JWT error message key
    JWT_ERROR_MESSAGE_KEY = "message"


class Development(Default):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_REFRESH_TOKEN_EXPIRES = False
    CORS_ORIGINS = ["*"]

    # Send emails to the console
    MAIL_BACKEND = "console"


class Testing(Default):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL") or "sqlite://"
    WORK_FACTOR = 4
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_REFRESH_TOKEN_EXPIRES = False
    CORS_ORIGINS = ["*"]


class Production(Default):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.sqlite")
    CORS_ORIGINS = ["UPDATE THIS WITH FRONTEND ORIGINS"]


app_environments = {
    "development": Development,
    "testing": Testing,
    "production": Production,
}

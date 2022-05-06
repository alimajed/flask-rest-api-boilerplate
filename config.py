from os import getenv


class ConfigFactory:
    def factory():
        env = getenv("FLASK_ENV", "development")
        if env in ["development"]:
            return Development()
        elif env in ["testing"]:
            return Testing()

    factory = staticmethod(factory)


class Config:
    """base config class contains same configurations in all environments"""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")


class Development(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")


class Testing(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_TEST_URI")

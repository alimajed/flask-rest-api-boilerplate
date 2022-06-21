from os import getenv


class ConfigFactory:
    def factory():
        env = getenv("FLASK_ENV", "development")
        if env in ["development"]:
            return Development()
        elif env in ["production"]:
            return Production()
        elif env in ["testing"]:
            return Testing()

    factory = staticmethod(factory)


class Config:
    """base config class contains same configurations in all environments"""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")


class Development(Config):
    DEBUG = True
    TESTING = False


class Production(Config):
    DEBUG = False
    TESTING = False


class Testing(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_TEST_URI")

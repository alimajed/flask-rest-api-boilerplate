from os import getenv


class ConfigFactory:
    def factory():
        env = getenv("FLASK_ENV", "development")

        if env in ["development"]:
            return Development()

    factory = staticmethod(factory)


class Config:
    """base config class contains same configurations in all environments"""
    pass

class Development(Config):
    DEBUG = True
    TESTING = False

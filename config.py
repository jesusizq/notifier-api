import os


class Config:
    DEBUG = False
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SLACK_BOT_TOKEN = os.environ.get("TEST_SLACK_BOT_TOKEN") or None
    SLACK_CHANNEL_ID = os.environ.get("TEST_SLACK_CHANNEL_ID") or None


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

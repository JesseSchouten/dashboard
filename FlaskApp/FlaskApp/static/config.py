class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "my_secret_key"

#    DB_NAME = "production-db"
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "Alkmaar12!"
    MYSQL_CURSORCLASS = "DictCursor"

    IMAGE_UPLOADS = "/static/images"

    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

#    DB_NAME = "development-db"
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "Alkmaar12!"
    MYSQL_CURSORCLASS = "DictCursor"

    IMAGE_UPLOADS = "/static/images"

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "Alkmaar12!"
    MYSQL_CURSORCLASS = "DictCursor"

    SESSION_COOKIE_SECURE = False

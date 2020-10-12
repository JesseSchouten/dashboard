class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "SECRET_KEY"

#    DB_NAME = "production-db"
    MYSQL_HOST = [MYSQL_HOST]
    MYSQL_USER = [MYSQL_USER]
    MYSQL_PASSWORD = [MYSQL_PASSWORD]
    MYSQL_CURSORCLASS = [MYSQL_CURSORCLASS]

    IMAGE_UPLOADS = "/static/images"

    # Secure cookies over HTTPS with SSL certificate.
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "SECRET_KEY"

#    DB_NAME = "development-db"
    MYSQL_HOST = [MYSQL_HOST]
    MYSQL_USER = [MYSQL_USER]
    MYSQL_PASSWORD = [MYSQL_PASSWORD]
    MYSQL_CURSORCLASS = [MYSQL_CURSORCLASS]

    IMAGE_UPLOADS = "/static/images"

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    MYSQL_HOST = [MYSQL_HOST]
    MYSQL_USER = [MYSQL_USER]
    MYSQL_PASSWORD = [MYSQL_PASSWORD]
    MYSQL_CURSORCLASS = [MYSQL_CURSORCLASS]

    SESSION_COOKIE_SECURE = False

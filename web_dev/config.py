class Config(object):
    """A base class."""
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """A development class."""
    ENV = 'development'
    SECRET_KEY = '9as8df(*S*8(das0ˆSˆD%5a67900SA(D*00'
    DEBUG = True

class TestingConfig(Config):
    """A testing class."""
    TESTING = True

class ProductionConfig(Config):
    """A production class."""
    SECRET_KEY = '98d0s809SD990AS)(dS&A&*d78(*&ASD08A'
from os import environ

import databases

DB_USER = environ.get("DB_USER", "user")
DB_PASSWORD = environ.get("DB_PASSWORD", "password")
DB_HOST = environ.get("DB_HOST", "localhost")

TESTING = environ.get("TESTING")

if TESTING:
    # Use separate DB for tests
    DB_NAME = "async-blogs-temp-for-test"
    TEST_SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    )
    database = databases.Database(TEST_SQLALCHEMY_DATABASE_URL)
else:
    DB_NAME = "async-blogs"
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    )
    database = databases.Database(SQLALCHEMY_DATABASE_URL)


SECRET_KEY = "0334065c-c3c5-47df-8053-5e11b934eaff"

SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}: {DB_PASS}@{DB_ADDR}/{DB_NAME}"\
        .format(DB_USER="postgres", DB_PASS="", DB_ADDR="127.0.0.1", DB_NAME="mapregister_db")

TEST_DATABASE_URI = "postgresql://{DB_USER}: {DB_PASS}@{DB_ADDR}/{DB_NAME}" \
    .format(DB_USER="postgres", DB_PASS="", DB_ADDR="127.0.0.1", DB_NAME="tests")

SECRET_KEY = "p9Bv<3Eid9%$i01"

SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}: {DB_PASS}@{DB_ADDR}/{DB_NAME}"\
        .format(DB_USER="postgres", DB_PASS="", DB_ADDR="127.0.0.1", DB_NAME="mapregister_db")

TEST_DATABASE_URI = "postgresql://{DB_USER}: {DB_PASS}@{DB_ADDR}/{DB_NAME}" \
    .format(DB_USER="postgres", DB_PASS="", DB_ADDR="127.0.0.1", DB_NAME="tests")
RUN_MODE = "TEST"  # "TEST" | "PRODUCTION"
DB_NAME = None

if RUN_MODE == "PRODUCTION":
    DB_NAME = "database_0.db"
elif RUN_MODE == "TEST":
    DB_NAME = "test_database.db"

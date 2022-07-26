import os
import time

from sqlalchemy import exc, create_engine


while 1:
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_host = os.getenv("POSTGRES_HOST")
    postgres_port = os.getenv("POSTGRES_PORT")
    postgres_db = os.getenv("POSTGRES_DB")
    database_uri = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
    try:
        e = create_engine(database_uri)
        e.execute("select 1")
    except exc.OperationalError:
        print("Waiting for database...")
        time.sleep(1)
    else:
        break

print("Database is ready!!")

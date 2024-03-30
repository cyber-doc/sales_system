import config
import psycopg2
tables = {}
tables['users'] = (
    """CREATE TABLE IF NOT EXISTS users (
      id SERIAL,
      first_name varchar(50) NOT NULL,
      last_name varchar(50) NOT NULL,
      email varchar(255) NOT NULL,
      password TEXT NOT NULL,
      create_date timestamp NOT NULL,
      last_update timestamp NOT NULL,
      PRIMARY KEY (id)
    ) """)


with psycopg2.connect(**config.config) as connection:
    with connection.cursor() as cursor:
        cursor.execute(tables["users"])
        connection.commit()

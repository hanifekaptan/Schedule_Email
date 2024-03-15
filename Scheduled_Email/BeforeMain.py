# BeforeMain.py must be run to create the database and tables before running the Main.py
# You must enter your user password for the PostgreSQL database in the userPassword variable.

import psycopg2

userPassword = ("secret")  # enter your password
conn = None
try:
    conn = psycopg2.connect(host = "localhost",
                            database="postgres",
                            user="postgres",
                            password=userPassword)
    conn.autocommit = True
    cur = conn.cursor()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)

cur.execute("CREATE DATABASE tttf;")

conn.commit()

cur.close()
conn = conn.close()

try:
    conn = psycopg2.connect(host = "localhost",
                            database="tttf",
                            user="postgres",
                            password=userPassword)
    cursor = conn.cursor()
except(Exception, psycopg2.DatabaseError) as error:
    print(error)

cursor.execute("""CREATE TABLE settings_info(
                email CHARACTER VARYING PRIMARY KEY NOT NULL,
                name CHARACTER VARYING NOT NULL,
                lastname CHARACTER VARYING NOT NULL,
                default_v BOOLEAN DEFAULT false)
            """)

cursor.execute("""CREATE TABLE letter_info(
                id SERIAL PRIMARY KEY NOT NULL,
                datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                email CHARACTER VARYING NOT NULL,
                title CHARACTER VARYING NOT NULL,
                message CHARACTER VARYING NOT NULL)
            """)

conn.commit()

cursor.close()
conn = conn.close()

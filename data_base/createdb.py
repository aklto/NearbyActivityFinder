from getpass import getpass
from mysql.connector import connect, Error

create_movies_table_query = """
CREATE TABLE movies(
    userid VARCHAR(16),
    location VARCHAR(100),
    liked vARCHAR(1000),
    unliked VARCHAR(1000)
)
"""

try:
    with connect(
        host="localhost",
        user="root",
        password="Qwe123123",
        database="testdb",
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(create_movies_table_query)
            connection.commit()
except Error as e:
    print(e)
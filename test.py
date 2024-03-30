import mysql.connector as mysql
from config import config
print('this is a test!!')
with (mysql.connect(**config)) as connection:
    with (connection.cursor(buffered=True)) as cursor:
        result = cursor.execute(
            "INSERT INTO sales_system.users (first_name, last_name, email, password, creat_date, last_update) VALUES (Nazanin, Tehrani, nazetehroon\@gmail.com, 2022-05-14, 2022-06-08)")
        connection.commit()
        print(result)

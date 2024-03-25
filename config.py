import mysql.connector as mysql
config = {
    'user': 'root',
    'password': 'Root@1234',
    'host': 'localhost',
    'database': 'sales_system'
}
connection = mysql.connect(**config)
cursor = connection.cursor()

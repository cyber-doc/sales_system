from config import cursor, connection

tables = {}
tables['users'] = (
    "CREATE TABLE `users` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `first_name` varchar(50) NOT NULL,"
    "  `last_name` varchar(50) NOT NULL,"
    "  `email` varchar(255) NOT NULL,"
    "  `password` varchar(255) NOT NULL,"
    "  `create_date` date NOT NULL,"
    "  `last_update` date NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")


cursor.execute(tables["users"])

connection.close()

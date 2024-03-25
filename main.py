from config import cursor, connection
runing = True
while runing:
    input = input("$ ")
    if input == "\\q":
        runing = False


connection.close()

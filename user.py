import re
from config import config
import bcrypt
import datetime
import psycopg2


# the user class (parent of .....)


class User:
    # the needed arguments for sign up
    def __init__(self, table) -> None:
        self.table = table

    sign_up_req_args = dict.fromkeys(
        ['first_name', 'last_name', 'email', 'password'])

    def sign_up(self, first_name: str, last_name: str, email: str, password: str) -> None:
        # Validation of inputs
        self.validation_loop(first_name, last_name, email, password)
        # checking if email doesn't exists
        if self.email_exists(email):
            print("the Email that you provide  is exists, please enter another email!")
            return
        # encrypt password
        encrypted_pass = self.encrypt_password(password)
        # iserting new values to databasee
        if self.inserter(first_name, last_name, email,
                         encrypted_pass, self.now_date()):
            print("your account is successfully created :) ")
            return
        else:
            print("Something went wrong please try again! ")
            return

    # this function return date and time of now
    def now_date(self) -> str:
        return str(round(datetime.datetime.now()))

    # this funcrion will check if the reauired email is exitss in db or not
    def email_exists(self, email: str) -> bool:
        query: str = """ SELECT * FROM users u WHERE u.email = %s"""
        data: tuple = (email,)
        result: list = self.query_builder(query, data, select=True)
        if len(result) == 0:
            return False
        else:
            return True
    # all the query needed in program is excuted in this function

    def query_builder(self, query: str, data: tuple, select=False) -> list | None:
        with psycopg2.connect(**config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                if select:
                    result = cursor.fetchall()
                    return result
                else:
                    connection.commit()
                    return
    # this function is for inserting data for sign up

    def inserter(self, first_name: str, last_name: str, email: str, password: bytes, date: str) -> bool:
        query = """INSERT INTO users (first_name, last_name, email, password, create_date, last_update) VALUES 
        (%s, %s, %s, %s, %s, %s)"""
        data = (first_name, last_name, email, password, date, date)
        self.query_builder(query, data)
        return True

    def encrypt_password(self, plain_password):
        # Encode the password as bytes
        encoded_password: bytes = plain_password.encode(
            'utf-8')
        salt: bytes = bcrypt.gensalt(12)
        encrypted_password = bcrypt.hashpw(encoded_password, salt)
        # Convert the hashed password back to a string
        return encrypted_password.decode('utf-8')

    def check_password(self, plain_password, encrypted_pass) -> bool:
        encoded_password = plain_password.encode(
            'utf-8')  # Encode plain_password as bytes
        if bcrypt.checkpw(encoded_password, encrypted_pass):
            return True
        return False
    # it has 3 methods of validating input data

    def validate(self, val_str, val_type) -> bool:
        # for names
        if val_type == 'name':
            pattern = r"^[a-zA-Z]{3,30}$"

        # for emails
        elif val_type == 'email':
            pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+){1,20}$"

        # for passwords
        elif val_type == 'password':
            pattern = r"^[a-zA-z0-9!@#$%^&*_-]{8,64}$"
        else:
            return False

        # match results
        match_result = re.match(pattern, val_str)
        # appending not valid inputs to not_valids list
        if match_result == None:
            return False
        else:
            return True
    # validation loop validate all of inputs that user insert fot sign up

    def validation_loop(self, first_name, last_name, email, password) -> None:
        if not self.validate(first_name, 'name'):
            print('the first name is not valid')
            return

        if not self.validate(last_name, 'name'):
            print('the last name is not valid')
            return

        if not self.validate(email, 'email'):
            print('the email is not valid')
            return

        if not self.validate(password, 'password'):
            print('the password is not valid')
            return

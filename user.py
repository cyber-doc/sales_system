import re
from config import config
import bcrypt
import datetime
import psycopg2


# the user class (parent of .....)


class User:
    # the needed arguments for sign up
    def __init__(self) -> None:

        self.table_name = "users"

        # Get column names from information_schema.columns
        query: str = """ SELECT column_name FROM information_schema.columns WHERE table_name = %s"""
        data: tuple = (self.table_name,)
        result: list = self.query_excuter(query, data, select=True)
        # Fetch all column names from the query result
        self.column_names = [row[0] for row in result] if result else []

    sign_up_req_args = dict.fromkeys(
        ['first_name', 'last_name', 'email', 'password'])
    sign_in_req_args = dict.fromkeys(
        ['email', 'password'])

    def sign_in(self, email, password):
        if not self.validation_loop(email=email, password=password):
            return
        if not self.email_exists(email):
            print("the combination of email and password is incorrect")
            return
        if not self.check_password(password, self.select_result[0]['password']):
            print("the combination of email and password is incorrect")
            return
        self.profile()

    def sign_up(self, first_name: str, last_name: str, email: str, password: str) -> None:
        # Validation of inputs
        if not self.validation_loop(first_name=first_name, last_name=last_name, email=email, password=password):
            return
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

    def profile(self):
        print(self.select_result[0])
    # this function return date and time of now

    def now_date(self) -> str:
        return str(datetime.datetime.now())

    # this funcrion will check if the reauired email is exitss in db or not
    def email_exists(self, email: str) -> bool:
        self.selector(email, condition='email')
        if len(self.select_result) == 0:
            return False
        else:
            return True
    # all the query needed in program is excuted in this function

    def query_excuter(self, query: str, data: tuple = None, select=False) -> list | None:
        with psycopg2.connect(**config) as connection:
            with connection.cursor() as cursor:
                if data == None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, data)
                if select:
                    result: list = cursor.fetchall()
                    return result
                else:
                    connection.commit()
                    return

    # this function is for inserting data for sign up
    def selector(self, value: str, condition='id') -> None:
        if condition == 'email':
            query: str = """ SELECT * FROM users WHERE email = %s"""
            data: tuple = (value,)
        result: list = self.query_excuter(query, data, select=True)
        self.select_result: list[dict] = self.convert_to_json(result)
        return

    def inserter(self, first_name: str, last_name: str, email: str, password: bytes, date: str) -> bool:
        query = """INSERT INTO users (first_name, last_name, email, password, create_date, last_update) VALUES 
        (%s, %s, %s, %s, %s, %s)"""
        data = (first_name, last_name, email, password, date, date)
        self.query_excuter(query, data)
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
        encoded_pass = plain_password.encode(
            'utf-8')  # Encode plain_password as bytes
        encoded_enc_pass = encrypted_pass.encode('utf-8')
        if bcrypt.checkpw(encoded_pass, encoded_enc_pass):
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

    def validation_loop(self, **args) -> bool:
        input_dict = args
        for key in input_dict:
            if key == 'first_name':
                field_name = 'first name'
                val_type: str = 'name'
            elif key == 'last_name':
                field_name = 'last name'
                val_type: str = 'name'
            elif key == 'email':
                field_name = 'email'
                val_type: str = 'email'
            elif key == 'password':
                field_name = 'password'
                val_type: str = 'password'
            else:
                print("something isn't right!")
                return False
            if not self.validate(input_dict[key], val_type):
                print(f'the {field_name} is not valid')
                return False
        else:
            return True

    def convert_to_json(self, result: list) -> list[dict]:
        json_result: list[dict] = []
        keys_list: list[str] = self.column_names
        rows = result
        for row in rows:
            json_result.append(dict(zip(keys_list, row)))
        return json_result

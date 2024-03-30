from user import User
runing = True
while runing:
    command = input("$ ")
    if command == 'sign up':
        user = User('users')
        args = user.sign_up_req_args
        for key in args:
            args[key] = input(f"Enter {key} : ")
        user.sign_up(**args)
    elif command == "\\q":
        runing = False

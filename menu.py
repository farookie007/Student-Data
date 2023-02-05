from sqlalchemy import or_
# custom imports
from utils import generate_token, generate_password_hash, send_email_code, validate_token,\
    check_password_hash, create_recovery_email, validate_email, SECRET_KEY
from school import Student
from database import engine, students, refresh, upload


def intro(student: Student):
    INTRO = """Enter any of the following commands:
                    'a' - to view your CGPA
                    'b' - to view the GPA of a particular level
                    'c' - to view the CGPA after a particular level
                    'd' - to view the session with the highest GPA
                    'e' - to view the session with the lowest GPA
                    'f' - to display your profile
                    
                    'u' - to UPLOAD/UPDATE your results
                    'i' - to get HELP
                    'q' - to LOGOUT
    """
    print(f"Welcome; {student.fullname if student.fullname else ''}")
    print(INTRO)


def view_cgpa(student: Student):
    print(f"Your CGPA is {student.cgpa:.2f}")


def view_sess_gpa(student: Student):
    level = input('Which Level (e.g 100, 200,...): ').lower()
    print(f"Your GPA for {level}L is {student.get_session(level).gpa:.2f}")


def view_highest_gpa(student: Student):
    s = student.high()
    print(f"You have the highest GPA in {s.level}L with {s.gpa:.2f}")


def view_lowest_gpa(student: Student):
    s = student.low()
    print(f"You have the lowest GPA in {s.level} with {s.gpa:.2f}")


def cgpa_after_level(student: Student):
    level = input('After which level (e.g 100, 200, ...): ')
    print(f"Your CGPA after {level}L is {student.get_cgpa_after(level):.2f}")


def display_profile(student: Student):
    decor = '######################################################################'
    if student.fullname:
        i = int(len(decor) / 2)
        print(decor)
        print('Name   :   '.rjust(i-7) + student.fullname.ljust(i))
        print('Matric Number   :   '.rjust(i-7) + student.matric_no.ljust(i))
        print('Department   :   '.rjust(i-7) + student.department.upper().ljust(i))
        print('Faculty   :   '.rjust(i-7) + student.faculty.upper().ljust(i))
        print('Current Level   :   '.rjust(i-7) + student.current_level.ljust(i))
        print('CGPA   :   '.rjust(i-7) + f'{student.cgpa:.2f}'.ljust(i))
        print(decor)


def menu():
    intr = """Enter any of the following commands:
                    'a': Log in
                    'b': Sign Up
                    'c': Recover Password
                    'd': Update the Database (Admin)
                    
                    'q': to Quit
    """
    print(intr)
    user_choice = input('>>> ').lower()

    while user_choice != 'q':
        if user_choice == 'a':  # Log In
            matric_no = input('Matric Number or Email: ').strip().upper()
            password = input('Password: ')
            login(matric_no, password)

        elif user_choice == 'b':    # Sign Up
            matric_no = input('Matric Number: ').strip().upper()
            email = input('Email (enter a valid email address for verification): ').strip().lower()
            if not validate_email(email):   # validates the email address provided by the user
                print('[ERROR]: Invalid email address')
                continue
            password1 = input('Password: ')
            password2 = input('Confirm Password: ')
            if password2 == password1:
                payload = generate_token(email)
                code = list(payload.keys())[0]
                msg = create_recovery_email(code, email, reset=False)
                send_email_code(msg)
                name, domain = email.split('@')
                code = input(f'Enter the code sent to {name.replace(name[-6:], "******")}@{domain}: ')
                while True:
                    try:
                        token = payload[code]
                        email = validate_token(token)
                        if email is None:
                            print('[ERROR]: The code you entered has expired! Retry.')
                        else:
                            signup(matric_no, email, password1)
                        break
                    except KeyError:
                        print('[ERROR]: You entered a wrong code!')
                        code = input(f'Re-Enter the code: ')
                        continue
            else:
                print('[WARNING]: Your password do not match. Try Again!')

        elif user_choice == 'c':    # Recover Password
            matric_no = input('Matric Number: ').strip().upper()
            reset_password(matric_no)

        elif user_choice == 'd':    # Update the Database (Admin)
            print("This function allows to batch update the database with all results files in the `results` folder.\n"
                  "[Note]: This operation requires admin access key.")
            key = input('Admin Key: ')
            if key == SECRET_KEY:
                refresh()
                print('***Updated...***')
            else:
                print('[Error]: Incorrect admin key')

        else:
            print('[ERROR]: Invalid Command. Try Again!')
        print(intr)
        user_choice = input('>>> ')


def student_menu(matric_no: str):
    student = Student(matric_no)

    operations = {
        'a': view_cgpa,
        'b': view_sess_gpa,
        'c': cgpa_after_level,
        'd': view_highest_gpa,
        'e': view_lowest_gpa,
        'f': display_profile,
        'i': intro
        }
    user_choice = 'f'
    while user_choice != 'q':
        if user_choice == 'u':
            print('**Uploading...**')
            upload(student.matric_no)
            student.update()
            user_choice = 'f'
        if student.fullname is None:    # i.e. the students have no data uploaded yet.
            print('[WARNING]: Your do not have any data uploaded yet.'
                  'Ensure the HTML files containing your results are in the `results` folder and upload them.')
        intro(student)
        operations[user_choice](student)
        user_choice = input('>>> ').lower()


def login(user_id: str, password: str):
    """This function logs the user into their account."""
    with engine.begin() as conn:
        s = students.select(). \
            where(or_(students.c.id == user_id.upper(), students.c.email == user_id.lower()))
        res = conn.execute(s).fetchone()
        if (res is not None) and (check_password_hash(password, res.password)):
            print('[INFO]: Login Successfully.')
            return student_menu(res.id)
        else:
            print('[ERROR]: Invalid Matric Number or Password.')


def reset_password(matric_no: str):
    """This function resets the user password and sends the reset code to their
    registered email."""
    with engine.begin() as conn:
        sel = students.select().where(students.c.id == matric_no)
        try:
            email = conn.execute(sel).fetchone().email
        except AttributeError:
            print(f"You have no account registered under `{matric_no}`.")
            return
    payload = generate_token(email)
    code = list(payload.keys())[0]
    msg = create_recovery_email(code, email)
    send_email_code(msg)
    name, domain = email.split('@')
    e = f'{name.replace(name[-6:], "******")}@{domain}'
    code = input(f'Enter the code sent to {e}: ')
    while True:

        try:
            token = payload[code]
            email = validate_token(token)

            if email is None:
                print('[ERROR]: The code you entered has expired! Retry.')

            else:
                password = input('New Password: ')
                n_password = input('Confirm New Password: ')
                if password != n_password:
                    print('[ERROR]: Your Password does not match!')
                else:
                    with engine.begin() as conn:
                        s = students.update().where(students.c.email == email). \
                            values(password=generate_password_hash(password))
                        conn.execute(s)
            break

        except KeyError:
            print('[ERROR]: You entered a wrong code!')
            code = input(f'Re-Enter the code sent to {e}: ')
            continue


def signup(matric_no: str, email: str, password: str):
    """This function helps new users to register their account, and stores their date in the database."""
    hashed_password = generate_password_hash(password)  # generates a hashed sequence of characters from the `password`.
    # the  `hashed password` is stored in the database and not the `password` for security purposes in case of attack
    with engine.begin() as conn:
        ins = students.insert().values(id=matric_no.upper(), email=email, password=hashed_password)
        conn.execute(ins)
        print('[INFO]: Account Created Successfully.')

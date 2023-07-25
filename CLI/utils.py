import re
import bcrypt
import random
import itsdangerous
import configparser

import pandas as pd
from errors.errors import MatchError

from smtplib import SMTP
from email.message import EmailMessage
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from typing import Dict, Tuple


config = configparser.ConfigParser()
config.read('configfile.ini')

EMAIL = config['email']['addr']
PASSWORD = config['email']['pwd']
SECRET_KEY = config['key']['secret_key']


def generate_password_hash(password: str) -> str:
    """Generates the `hashed password` from `password`.
    : return: str"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')


def check_password_hash(password: str, hashed_password: str) -> bool:
    """This function checks the `password` and compares it with the `hashed password`
    from the database.
    : return: bool"""
    return bcrypt.checkpw(password.encode(), hashed_password.encode('utf-8'))


def send_email_code(message: EmailMessage):
    """This function connects to the SMTP server, and sends the email `message`
    to the user - `recv`."""
    server = SMTP(host='smtp.googlemail.com', port=587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.send_message(message)


# noinspection SpellCheckingInspection
def create_recovery_email(code: str, recv: str, sender: str = 'noreply@gmail.com', reset=True) -> EmailMessage:
    """This function composes the reset password / email verification message to be sent to the 'recv'.
    : return: email object"""
    content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title></title>
    </head>
    <body bgcolor="#fff" style="font-family: 'Calibri';font-weight: 200px;font-size: 25px;margin-top:0;
    margin-bottom:0 ;margin-right:0 ;margin-left:0 ;padding-top:0px;
    padding-bottom:0px;padding-right:0px;padding-left:0px;background-color:#e1e5e8;">
        <center style="width:100%;table-layout:fixed;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;
        background-color:#fff;">
        <div style="max-width:600px;margin-top:0;margin-bottom:0;margin-right:auto;margin-left:auto;">
            <p>Your {"password reset" if reset else "email verification"} pin is:<br>
            <span style="font-size: 65px; color: #2222ff;">{code}</span><br><br>
            <small><span style="color: #ff0000">NOTE:</span> This code expires after <b>10 minutes</b>.<br>
            Please, {"ignore this message if you didn't request for a change of password." if reset else
            "enter the pin to verify your email."}</small></p>
        </div>
        </center>
    </body>
    </html>
    '''
    email = EmailMessage()

    email['Subject'] = f'{"Password Reset" if reset else "Account Verification"} Pin'
    email['From'] = sender
    email['To'] = recv

    email.set_content(content, subtype='html')
    return email


def generate_token(email: str) -> Dict[str, bytes]:
    """This function generates a token which expires after 10 minutes. This token is
    to reset the password."""
    s = Serializer(SECRET_KEY, expires_in=600)  # creates a Serializer which expires in 10 minutes
    token = s.dumps(email)
    code = str(random.randint(100000, 999999))
    return {code: token}


def validate_token(token: bytes):
    """This function validates the `token` and checks if it is still valid (i.e not expired yet)."""
    s = Serializer(SECRET_KEY)
    try:
        email = s.loads(token)
        return email
    except itsdangerous.exc.SignatureExpired:
        return None


def validate_email(email: str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return bool(re.fullmatch(regex, email))

def parse_html(file, sessional=True) -> Tuple:
    """
    This function parses the HTML file containing the results of a Student (esp. University of Ilorin)
    into a pandas DataFrame and creates a Semester object for each individual semester contained in the result.
    Ensure the HTML files are stored in a folder named 'results' and the filenames are named in ascending order 
    according to their corresponding years to enable the function locate it.
    :return: List[pandas.DataFrame]
    """
    grade = {
        'A': 5,
        'B': 4,
        'C': 3,
        'D': 2,
        'E': 1,
        'F': 0
        }
    matric, name, fac, dept, level = pd.read_html(file)[0][1]
    
    # extracting the session id
    with open(file, 'r') as f:
        content = f.read()
        session_id = re.search('\d\d\d\d/\d\d\d\d', content).group()

    dfs = pd.read_html(file, header=1, index_col=1)
    for df in dfs[1:]:
        df.drop(columns=['Unnamed: 9', 'S/No.'], index='Total', inplace=True)
        df.dropna(inplace=True)
        if fac == 'Engineering and Technology' and level == '100':
            # This handles the complications with Engineering and Technology 100L results where only GNS matters.
            df.drop(labels=[title for title in df.index if not title.startswith('GNS')], axis=0, inplace=True)
        df['Gradient'] = pd.Series(
            [df.loc[f]['Unit'] * grade[df.loc[f]['Grade']] for f in df.index],
            index=df.index,
            dtype='int8'
            )
    if sessional:
        return dfs[1:], session_id, name, matric, fac, dept, level
    return dfs[-1], session_id, name, matric, fac, dept, level

def parse(file, sessional=True) -> Tuple:
    """
    This function parses the HTML file containing the results of a Student (esp. University of Ilorin)
    into a pandas DataFrame and creates a Semester object for each individual semester contained in the result.
    Ensure the HTML files are stored in a folder named 'results' and the filenames are named in ascending order 
    according to their corresponding years to enable the function locate it.
    :return: List[pandas.DataFrame]
    """
    grade = {
        'A': 5,
        'B': 4,
        'C': 3,
        'D': 2,
        'E': 1,
        'F': 0
        }
    matric, name, fac, dept, level = pd.read_html(file)[0][1]
    dfs = pd.read_html(file, header=1, index_col=1)
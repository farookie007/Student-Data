import re
import bcrypt
import random
import itsdangerous
import configparser
from smtplib import SMTP
from email.message import EmailMessage
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from typing import Dict

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


# noinspection SpellCheckingInspection
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
    <body bgcolor="#e1e5e8" style="font-family: 'Calibri';font-weight: 200px;font-size: 25px;margin-top:0;
    margin-bottom:0 ;margin-right:0 ;margin-left:0 ;padding-top:0px;
    padding-bottom:0px;padding-right:0px;padding-left:0px;background-color:#e1e5e8;">
        <center style="width:100%;table-layout:fixed;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;
        background-color:#e1e5e8;">
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

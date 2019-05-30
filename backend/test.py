import uuid as uuid_helper
import sqlite3
import hashlib
from validate_email import validate_email

def is_unique(key, value):
    conn = sqlite3.connect('/root/beerpong/beerpong.db')
    c = conn.cursor()
    if c.execute("""SELECT 1 FROM users WHERE ? = ?;""", (str(key), str(value))) is 0:
        conn.commit()
        conn.close()
        return True
    else:
        conn.commit()
        conn.close()
        return False

def check_username(username):
    if not str(username).__len__() > 5:
        return 'username: ' + str(username) + ' DENIED (<6 chars)'
    if not is_unique('username', username):
        return 'username: ' + str(username) + ' DENIED (not unique)'
    return 'username: ' + str(username) + ' IS FINE'

def check_mail(mail):
    return validate_email(str(mail), verify=True)

def main():
    uuid = str(uuid_helper.uuid4())
    username = input('username: ')
    mail = input('mail: ')
    passwd = hashlib.sha512(str(input('passwd: ')).encode()).hexdigest()

    username_check = check_username(username)
    if username_check is 'username: ' + str(username) + ' IS FINE':
        print(username_check)
    else:
        print(username_check)

    if check_mail(mail):
        print('email: ' + str(mail) + ' IS FINE')
    else:
        print('email: ' + str(mail) + ' DENIED')

main()
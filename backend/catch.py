def empty_login(username, passwd):
    if str(username) is "" and str(passwd) is "":
        return True
    else:
        return False


def empty_mail(mail):
    if mail is None or mail == "":
        return True
    else:
        return False

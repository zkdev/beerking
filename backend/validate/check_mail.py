from validate_email import validate_email
from ..enums.enums import Mail


def main(mail):
    if validate_email(str(mail), verify=True):
        return Mail.FINE
    else:
        return Mail.NOT_EXISTING

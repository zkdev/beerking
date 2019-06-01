from validate_email import validate_email
from logger import log
from enums.enums import Mail


def main(mail):
    if validate_email(str(mail), verify=True):
        log.info('\"' + str(mail) + '\" as mail accepted')
        return Mail.FINE
    else:
        log.info('\"' + str(mail) + '\" as mail rejected (not existing)')
        return Mail.NOT_EXISTING

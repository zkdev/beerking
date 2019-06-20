import datetime


def info(msg):
    print('[\033[1;32;40mINFO\033[0;37;40m][' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ']: ' + str(msg))


def error(msg):
    print('[\033[0;31;40mERROR\033[0;37;40m][' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ']: ' + str(msg))


def security(msg):
    print('[\033[1;31;40mSECURITY\033[0;37;40m][' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ']: ' + str(msg))

import datetime


def info(msg):
    print('[INFO][' + str(datetime.datetime.now()) + ']: ' + str(msg))


def error(msg):
    print('[ERROR][' + str(datetime.datetime.now()) + ']: ' + str(msg))

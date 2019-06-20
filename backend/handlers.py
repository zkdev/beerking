import json
from flask import request


from . import validate, sql, elo, match, log
from .enums import User, Match, Reason, Friends, UniqueMode


def create_user(conn, userid, username, mail, passwd):
    if validate.mail_is_fine(mail):
        m = User.WILL_CREATE
    else:
        m = User.WONT_CREATE

    if validate.catch_empty_mail(mail):
        mail = ""
        m = User.WILL_CREATE

    if validate.username_is_fine(conn, username):
        u = User.WILL_CREATE
    else:
        u = User.WONT_CREATE

    if m is User.WILL_CREATE and u is User.WILL_CREATE:
        sql.create_user(conn, userid, username, mail, passwd, elo.initial_elo())
        log.info('User created. Username: ' + str(username))
        return User.CREATED
    else:
        if m is not User.WILL_CREATE:
            return Reason.MAIL_DOESNT_EXIST
        elif u is not User.WILL_CREATE:
            if validate.is_unique(conn, UniqueMode.USERNAME, username):
                return Reason.USERNAME_TOO_SHORT
            else:
                return Reason.USERNAME_NOT_UNIQUE


def auth(conn, username, passwd):
    c = conn.cursor()
    r = sql.login(c, username, passwd)
    if r is None:
        return False
    else:
        return True


def update_mail(conn, username, passwd, mail):
    r = User.MAIL_UPDATE_FAILED
    if auth(conn, username, passwd):
        userid = sql.get_userid(conn, username).fetchone()[0]
        if validate.mail_is_fine(mail):
            sql.update_user_mail(conn, userid, mail)
            r = User.MAIL_UPDATED
    return r


def confirm_match(conn):
    for single_match in json.loads(request.form.get('matches')):
        matchid = single_match.get('matchid')
        if single_match.get('confirmed') is True:
            match.confirm_match(conn, matchid)
        sql.remove_pending_match(conn, matchid)
    return Match.CONFIRMED


def leaderboard(conn, userid):
    arr = []
    lb = sql.leaderboard(conn).fetchall()
    fl = sql.get_friends(conn, userid).fetchall()
    for entry in lb:
        username = entry[1]
        elo = entry[2]
        friendids = [elem[1] for elem in fl]
        if entry[0] in friendids:
            isfriend = True
        else:
            isfriend = False
        arr.append({"username": username, "elo": elo, "isfriend": isfriend})
    return arr


def user_history(conn, username):
    userid = sql.get_userid(conn, username).fetchone()[0]
    h = sql.get_user_history(conn, userid).fetchall()
    return h


def add_friend(conn, userid, friendname):
    if not validate.is_unique(conn, UniqueMode.USERNAME, friendname):
        friendid = sql.get_userid(conn, friendname).fetchone()[0]
        if sql.is_friend(conn, userid, friendid).fetchone() is None:
            if str(userid) == str(friendid):
                r = Reason.SAME_AS_USER
            else:
                sql.add_friend(conn, userid, friendid)
                r = Friends.ADDED
        else:
            r = Reason.FRIENDS_ALREADY
    else:
        r = Reason.FRIEND_DOESNT_EXIST
    return r


def remove_friend(conn, userid, friendname):
    friendid = sql.get_userid(conn, friendname).fetchone()[0]
    sql.remove_friend(conn, userid, friendid)

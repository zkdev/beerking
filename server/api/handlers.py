from flask import request

import json
import datetime

import validate
import sql
import elo_handler
import match
import response as response
from enums import User, Match, Reason, Friends, UniqueMode


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
        sql.create_user(conn, userid, username, mail, passwd, elo_handler.initial_elo(), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return response.build({"user_created": True}, statuscode=201)
    else:
        if m is not User.WILL_CREATE:
            return response.build({"user_created": False, "mail_exists": False}, statuscode=400)
        elif u is not User.WILL_CREATE:
            if validate.is_unique(conn, UniqueMode.USERNAME, username):
                return response.build({"user_created": False, "username_too_short": True}, statuscode=400)
            else:
                return response.build({"user_created": False, "username_unique": False}, statuscode=400)


def auth(conn, username, passwd):
    c = conn.cursor()
    r = sql.login(c, username, passwd)
    if r is None:
        return False
    else:
        return True


def update_mail(conn, username, passwd, mail):
    resp = response.build({"mail_updated": False}, statuscode=403)
    if auth(conn, username, passwd):
        userid = sql.get_userid(conn, username).fetchone()[0]
        if validate.mail_is_fine(mail):
            sql.update_user_mail(conn, userid, mail)
            resp = response.build({"mail_updated": True}, statuscode=202)
    return resp


def confirm_match(conn):
    for single_match in json.loads(request.form.get('matches')):
        matchid = single_match.get('matchid')
        if single_match.get('confirmed') is True:
            match.confirm_match(conn, matchid)
        sql.remove_pending_match(conn, matchid)
    return response.build({"matches_confirmed": True}, statuscode=201)


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
        userid = sql.get_userid(conn, username).fetchall()[0][0]
        matches = sql.count_matches(conn, userid).fetchall()[0][0]
        display = False
        if matches >= 1:
            display = True
        arr.append({"username": username, "elo": elo, "isfriend": isfriend, "display": display})
    return arr


def user_history(conn, username):
    userid = sql.get_userid(conn, username).fetchone()[0]
    h = sql.get_user_history(conn, userid).fetchall()
    arr = []
    for entry in h:
        host = entry[0]
        friend = entry[1]
        enemy1 = entry[2]
        enemy2 = entry[3]
        winner = entry[4]
        date_data = entry[5]
        arr.append({"host": host, "friend": friend, "enemy1": enemy1, "enemy2": enemy2, "winner": winner,
                    "datetime": date_data})
    return response.build({"matches": arr}, statuscode=200)


def add_friend(conn, userid, friendname):
    if not validate.is_unique(conn, UniqueMode.USERNAME, friendname):
        friendid = sql.get_userid(conn, friendname).fetchone()[0]
        if sql.is_friend(conn, userid, friendid).fetchone() is None:
            if str(userid) == str(friendid):
                return response.build({"friend_added": False}, statuscode=400)
            else:
                sql.add_friend(conn, userid, friendid)
                return response.build({"friend_added": True}, statuscode=201)
        else:
            return response.build({"friend_added": False}, statuscode=400)
    else:
        return response.build({"friend_added": False}, statuscode=400)


def remove_friend(conn, userid, friendname):
    friendid = sql.get_userid(conn, friendname).fetchone()[0]
    sql.remove_friend(conn, userid, friendid)


def get_friends(conn, userid):
    fl = sql.get_friends(conn, userid).fetchall()
    arr = []
    for entry in fl:
        friendname, friendid = entry
        arr.append({"friend": friendid, "friendname": friendname})
    return response.build({"friends": arr}, statuscode=200)

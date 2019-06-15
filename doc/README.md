# Backend Documentation
| router | method | header | param | body | description | response |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | 
| /user/create | POST | version ||username, mail, passwd, version | creates a user | `user_created`<br>`username_unique`<br>`username_too_short`<br>`mail_exists`
| /user/mail/update | PUT | version || username, mail, passwd, version | updates the users mail adress | `mail_updated`
| /users/profile | GET | version | username, passwd, version | | retrieves the user's profile | `auth`<br>`user_id`<br>`mail`
| /match/1v1 | POST | version || host, enemy, winner, version | starts a new 1v1 match | `match_started`
| /match/2v2 | POST | version || host, friend, enemy1, enemy2, winner, version | starts a new 2v2 match | `match_started`
| /match/pending | GET | version |userid, version || retrieves pending matches to confirm | `matches_received`<br>`matches.matchid`<br>`matches.hostname`<br>`matches.winner`<br>`matches.datetime`
| /match/confirm | POST | version || username, passwd, version | confirms a pending match | `matches_confirmed`
| /leaderboard | GET | version |userid, version || retrieves the leaderboard | `leaderboard.username`<br>`leaderboard.elo`<br>`leaderboard.isfriend`
| /user/history | GET | version |username, passwd, version || retrieves the user's history | `matches.host`<br>`matches.friend`<br>`matches.enemy1`<br>`matches.enemy2`<br>`matches.winner`<br>`matches.datetime`
| /check/userid | GET | version |userid, version || validates whether an userid exists or not | `userid_exists`
| /friends | GET | version | userid || retrieves the user's friendlist | `friends.friend`<br>`friends.friendname`
| /friends/add | POST | version || userid, friendname, version | adds a friend on the user's friendlist | `friend_added`
| /friends/remove | DELETE | version || userid, friendname, version | removes a friend from the user's friendlist | `friend_removed`

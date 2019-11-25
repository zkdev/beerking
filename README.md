# BeerKing
## Version
![Version](https://img.shields.io/badge/version-1.2.1-brightgreen.svg?style=flat-square)
![Version](https://img.shields.io/badge/release-release-green.svg?style=flat-square)

## Status
**Backend API:** ![Backend API](https://img.shields.io/badge/status-offline-red.svg?style=flat-square)<br>
**Backend API DEV:** ![Backend API DEV](https://img.shields.io/badge/status-offline-red.svg?style=flat-square)<br>
**Backend Web-UI:** ![Backend Web-UI](https://img.shields.io/badge/status-offline-red.svg?style=flat-square)<br>
**Backend Web-UI DEV:** ![Backend Web-UI DEV](https://img.shields.io/badge/status-offline-red.svg?style=flat-square)<br>

# Connection Information
**Frontend**:  beerking-ui.zeekay.dev:13003<br>
**Web-UI-DEV**: beerking-ui-dev.zeekay.dev:13004<br>
**Backend**:  beerking-api.zeekay.dev:5000<br>
**Backend DEV**: beerking-api-dev.zeekay.dev:5003<br>

# Backend Documentation
| router | method | header | param | body | description | response |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | 
| /status | GET | version || | checks server status | `{"status": "available"}`
| /user/create | POST | version ||username, mail, passwd | creates a user | `user_created`<br>`username_unique`<br>`username_too_short`<br>`mail_exists`
| /user/mail/update | PUT | version || username, mail, passwd | updates the users mail adress | `mail_updated`
| /user/profile | GET | version | username, passwd | | retrieves the user's profile | `auth`<br>`userid`<br>`mail`<br>`server_message`
| /check/userid | GET | version |userid || validates whether an userid exists or not | `userid_exists`
| /user/history | GET | version |username, passwd || retrieves the user's history | `matches.host`<br>`matches.friend`<br>`matches.enemy1`<br>`matches.enemy2`<br>`matches.winner`<br>`matches.datetime`
| /match/1v1 | POST | version || host, enemy, winner | starts a new 1v1 match | `match_started`
| /match/2v2 | POST | version || host, friend, enemy1, enemy2, winner | starts a new 2v2 match | `match_started`
| /match/pending | GET | version |userid || retrieves pending matches to confirm | `matches_received`<br>`matches.matchid`<br>`matches.hostname`<br>`matches.winner`<br>`matches.datetime`
| /match/confirm | POST | version || username, passwd | confirms a pending match | `matches_confirmed`
| /leaderboard | GET | version |userid || retrieves the leaderboard | `leaderboard.username`<br>`leaderboard.elo`<br>`leaderboard.isfriend`
| /friends | GET | version | userid || retrieves the user's friendlist | `friends.friend`<br>`friends.friendname`
| /friends/add | POST | version || userid, friendname | adds a friend on the user's friendlist | `friend_added`<br>`friend_equal_user`
| /friends/remove | DELETE | version || userid, friendname | removes a friend from the user's friendlist | `friend_removed`

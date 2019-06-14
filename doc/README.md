# Backend Documentation
| router | method | param | body | description |
| ------ | ------ | ------ | ------ | ------ |
| /users/creation | POST |  | username, mail, passwd | creates a user
| /users/mail/update | PUT | | username, mail, passwd | updates the users mail adress
| /users/login | GET | username, passwd | | authenticates the user
| /match/1v1 | POST |  | host, enemy, winner | starts a new 1v1 match
| /match/2v2 | POST |  | host, friend, enemy1, enemy2, winner | starts a new 2v2 match
| /match/pending | GET | userid | | retrieves pending matches to confirm
| /match/confirm | POST |  | username, passwd | confirms a pending match
| /match/leaderboard | GET | userid | | retrieves the leaderboard
| /users/history | GET | username, passwd | | retrieves the user's history
| /userid | GET | userid |  | validates whether an userid exists or not
| /friends | GET | userid |  | retrieves the user's friendlist
| /friends/add | POST |  | userid, friendid | adds a friend on the user's friendlist
| /friends/remove | DELETE |  | userid, friendid | removes a friend from the user's friendlist
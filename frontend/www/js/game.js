var players;


function startNewGame(event, team_size) {
    document.getElementsByTagName("body")[0].className = "body_bg_invisible";
    document.getElementById("start_game").style.visibility = "hidden";
    team_size = team_size * 2 - 1;
    var ids = [];
    try {
        var callback = function(err, text) {
            window.QRScanner.destroy();
            if (err) {
                window.location = "./main.html";
                throw "Scan error";
            } else {
                var name = text.split("[&!?]")[1];
                var uuid = text.split("[&!?]")[0];
                for (var i = 0; i < ids.length; i++) {
                    if (ids[i].uuid === uuid) {
                        SpinnerPlugin.activityStop();
                        window.location = "./main.html";
                    }
                }
                var request = {};
                request.userid = uuid;
                SpinnerPlugin.activityStart("Checke Spieler...", options);
                $.ajax({
                    type: "GET",
                    url: base_url + "/check/userid",
                    data: request,
                    complete: function(response) {
                        SpinnerPlugin.activityStop();
                        navigator.notification.alert(name, null, "Spieler gescannt");
                        if (JSON.parse(response.responseText).userid_exists === true) {
                            ids.push({ name: name, uuid: uuid });
                            if (ids.length === team_size) {
                                displayTeam(ids, team_size);
                            } else {
                                window.QRScanner.scan(callback);
                            }
                        } else {
                            window.location = "./main.html";
                        }
                    }
                });
            }
        }
        window.QRScanner.scan(callback);
        window.QRScanner.show();
    } catch (e) {
        document.getElementById("start_game").style.visibility = "visible";
        document.getElementsByTagName("body")[0].className = "body_bg";
    }
}

function displayTeam(ids, team_size) {
    try {
        window.QRScanner.destroy();
    } catch (e) {
        console.log("QR Reader error: " + e);
    }
    document.getElementsByTagName("body")[0].classList = "body_bg";
    if ((ids.length === team_size) && (team_size === 3)) {
        players = ids;
        var teams = document.getElementById("team");
        var div = document.createElement("DIV");
        div.innerText = "Wähle deinen Partner:";
        div.className = "team_ch";
        teams.appendChild(div);

        var sel = document.createElement("DIV");
        var html = "<select style='font-size: 20px;width: 80vw;border-color: #B3121D;border-width: 2px;' id='select_teammate' onchange='if (this.selectedIndex) chooseTeammate();'><option disabled selected value> -- Wählen -- </option>";
        for (var i = 0; i < ids.length; i++) {
            html += "<option value='"+ ids[i].name +"'>" + ids[i].name + "</option>";
        }
        html += "</select>";
        sel.innerHTML = html;
        div.appendChild(sel);
        
    } else if (ids.length === team_size && team_size === 1) {
        //start game ajax
        players = ids;
        document.getElementById("active_game").style.visibility = "visible";
        document.getElementById("select_winner").options[1].innerText = window.localStorage.getItem("user");
        document.getElementById("select_winner").options[2].innerText = ids[0].name;

    }
    return;
}

function sendWinner() {
    var game = {};
    ids = players;
    players = undefined;
    game.host = window.localStorage.getItem("uuid");
    if (ids.length === 3) {
        game.friend = ids[0].uuid;
        game.enemy1 = ids[1].uuid;
        game.enemy2 = ids[2].uuid;
        game.winner = document.getElementById("select_winner").value;

        SpinnerPlugin.activityStart("Schicke Gewinner...", options);
        $.ajax({
            type: "POST",
            url: base_url + "/match/2v2",
            data: game,
            complete: function(response) {
                SpinnerPlugin.activityStop();
                window.location = "./main.html";
            },
            dataType: "text/json"
        })
    } else {
        game.enemy = ids[0].uuid;
        game.winner = document.getElementById("select_winner").value;
        SpinnerPlugin.activityStart("Schicke Gewinner...", options);
        $.ajax({
            type: "POST",
            url: base_url + "/match/1v1",
            data: game,
            complete: function(response) {
                SpinnerPlugin.activityStop();
                window.location = "./main.html";
            },
            dataType: "text/json"
        })
    }
    return;
}

function chooseTeammate() {
    var name = document.getElementById("select_teammate").value;
    var players_akt = [];
    var index = 0;
    for (var i = 0; i < players.length; i++) {
        if (players[i].name === name) {
            players_akt.push(players[i]);
            index = i;
        }
    }
    if (index === 0) {
        players_akt.push(players[1]);
        players_akt.push(players[2]);
    } else if (index === 1) {
        players_akt.push(players[0]);
        players_akt.push(players[2]);

    } else {
        players_akt.push(players[0]);
        players_akt.push(players[1]);
    }
    document.getElementById("select_teammate").disabled = "true";
    players = players_akt;
    document.getElementById("active_game").style.visibility = "visible";
    document.getElementById("select_winner").options[1].innerText = window.localStorage.getItem("user") + " " + players[0].name;
    document.getElementById("select_winner").options[2].innerText = players[1].name + " " + players[2].name;
}

function onWinnerSelected() {
    var v = document.getElementById("select_winner").value;
    if (v == 0) {
        document.getElementById("winner").innerText = "DU HAST GEWONNEN";
        document.getElementById("winner").style = "color: green;font-size: larger;font-weight:bold";
        document.getElementById("send_winner").disabled = false;
    } else if (v == 1) {
        document.getElementById("winner").innerText = "DU HAST VERLOREN";
        document.getElementById("winner").style = "color: red;font-size: larger;font-weight:bold";
        document.getElementById("send_winner").disabled = false;
    }
}
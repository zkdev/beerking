var players;
var scanner;
var cams;

function startNewGame(event, team_size) {
    document.getElementById("cont").style.display = "none";
    document.getElementById("start_game").style.visibility = "hidden";
    document.getElementById("preview").className = "body_bg_invisible";
    document.getElementById("prev").className = "";
    team_size = team_size * 2 - 1;
    var ids = [];
    scanner = new Instascan.Scanner({ video: document.getElementById('prev') , mirror:false});
    scanner.addListener('scan', function (content) {
        scanner.stop();
        if (content === "") {
            window.location = "./main.html";
            throw "Scan error";
        } else {
            var name = content.split("[&!?]")[1];
            var uuid = content.split("[&!?]")[0];
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
                complete: function (response) {
                    SpinnerPlugin.activityStop();
                    navigator.notification.alert(name, null, "Spieler gescannt");
                    if (JSON.parse(response.responseText).userid_exists === true) {
                        ids.push({ name: name, uuid: uuid });
                        if (ids.length === team_size) {
                            displayTeam(ids, team_size);
                        } else {
                            scanner.start(cams[cams.length-1]);
                        }
                    } else {
                        window.location = "./main.html";
                    }
                }
            });
        }
    });
    if (cams === undefined) {
        Instascan.Camera.getCameras().then(function (cameras) {
            cams = cameras;
            if (cameras.length > 0) {
                scanner.start(cameras[cameras.length-1]);
            } else {
                console.error('No cameras found.');
            }
        }).catch(function (e) {
            document.getElementById("start_game").style.visibility = "visible";
            document.getElementById("cont").style.display = "block";
            document.getElementById("preview").className = "invis";
            document.getElementById("prev").className = "invis";
        });
    } else {
        scanner.start(cams[cams.length-1]);
    }
}

function displayTeam(ids, team_size) {
    document.getElementById("preview").className = "invis";
    document.getElementById("prev").className = "invis";
    document.getElementById("cont").style.display = "block";
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
            html += "<option value='" + ids[i].name + "'>" + ids[i].name + "</option>";
        }
        html += "</select>";
        sel.innerHTML = html;
        div.appendChild(sel);

    } else if (ids.length === team_size && team_size === 1) {
        //start game ajax
        players = ids;
        document.getElementById("active_game").style.visibility = "visible";
        document.getElementById("active_game").style.marginTop = "-100%";
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
            complete: function (response) {
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
            complete: function (response) {
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
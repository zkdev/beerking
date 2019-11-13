var players;
var scanner;
var cams;
var camIndex = 0;

function startNewGame(event, team_size) {
    $("#cont").css("display", "none");
    $("#start_game").css("visibility", "hidden");
    $("#preview").attr("class", "body_bg_invisible");
    $("#prev").attr("class", "");
    team_size = team_size * 2 - 1;
    var ids = [];
    scanner = new Instascan.Scanner({ video: document.getElementById('prev'), mirror: false });
    scanner.addListener('scan', function (content) {
        scanner.stop();
        if (content === "") {
            window.location = "./main.html";
            throw "Scan error";
        } else {
            var name = content.split("[&!?]")[1];
            var uuid = content.split("[&!?]")[0];
            for (let i = 0; i < ids.length; i++) {
                if (ids[i].uuid === uuid) {
                    //Scanned user twice ...
                    SpinnerPlugin.activityStop();
                    window.location = "./main.html";
                }
            }
            let request = {
                userid: uuid
            };
            SpinnerPlugin.activityStart(i18n.check_spieler_message, options);
            $.ajax({
                type: "GET",
                url: base_url + "/check/userid",
                data: request,
                complete: function (response) {
                    SpinnerPlugin.activityStop();
                    navigator.notification.alert(name, null, i18n.player_scanned_header);
                    try {
                        var resp = JSON.parse(response.responseText);
                    } catch (e) { }
                    if (resp && resp.userid_exists === true) {
                        ids.push({
                            name: name,
                            uuid: uuid
                        });
                        if (ids.length === team_size) {
                            displayTeam(ids, team_size);
                        } else {
                            scanner.start(cams[camIndex]);
                        }
                    } else {
                        window.location = "./main.html";
                    }
                }
            });
        }
    });
    if (!cams) {
        Instascan.Camera.getCameras().then(function (cameras) {
            cams = cameras;
            if (cameras.length > 0) {
                scanner.start(cameras[camIndex]);
            }
        }).catch(function (e) {
            hideCameraViews();
        });
    } else {
        scanner.start(cams[camIndex]);
    }
}

function hideCameraViews() {
    $("#start_game").css("visibility", "visible");
    $("#cont").css("display", "block");
    $("#preview").attr("class", "invis");
    $("#prev").attr("class", "invis");
}

function displayTeam(ids, team_size) {
    hideCameraViews();
    $("#start_game").css("visibility","hidden");
    if (ids.length === team_size && team_size === 3) {
        players = ids;
        let teams = document.getElementById("team");
        var div = document.createElement("DIV");
        div.innerText = i18n.chose_teammate;
        div.className = "team_ch";
        teams.appendChild(div);
        var html = "<select style='font-size: 20px;width: 80vw;border-color: #B3121D;border-width: 2px;' id='select_teammate' onchange='if (this.selectedIndex) chooseTeammate();'><option disabled selected value> -- " + i18n.choose + " -- </option>";
        for (let i = 0; i < ids.length; i++) {
            html += "<option value='" + ids[i].name + "'>" + ids[i].name + "</option>";
        }
        html += "</select>";
        let sel = document.createElement("DIV")
        sel.innerHTML = html;
        div.appendChild(sel);
    } else if (ids.length === team_size && team_size === 1) {
        players = ids;
        $("#active_game").css({ "visibility": "visible", "margin-top": "-100%" });
        $("#select_winner option:contains('Mein Team')").text(window.localStorage.getItem("user"));
        $("#select_winner option:contains('Gegner Team')").text(ids[0].name);
    }
    return;
}

function sendWinner() {
    var game = {
        host: window.localStorage.getItem("uuid"),
        winner: $("#select_winner").val()
    };
    if (players.length === 3) {
        game.friend = players[0].uuid;
        game.enemy1 = players[1].uuid;
        game.enemy2 = players[2].uuid;
        SpinnerPlugin.activityStart(i18n.send_winner, options);
        $.ajax({
            type: "POST",
            url: base_url + "/match/2v2",
            data: game,
            complete: function (response) {
                players = undefined;
                SpinnerPlugin.activityStop();
                window.location = "./main.html";

            },
            dataType: "text/json"
        })
    } else {
        game.enemy = players[0].uuid;
        SpinnerPlugin.activityStart(i18n.send_winner, options);
        $.ajax({
            type: "POST",
            url: base_url + "/match/1v1",
            data: game,
            complete: function (response) {
                players = undefined;
                SpinnerPlugin.activityStop();
                window.location = "./main.html";
            },
            dataType: "text/json"
        })
    }
    return;
}

function chooseTeammate() {
    var name = $("#select_teammate").val();
    var players_akt = [];
    for (let i = 0; i < players.length; i++) {
        if (players[i].name === name) {
            players_akt.unshift(players[i]);
        }else{
            players_akt.push(players[i]);
        }
    }
    players = players_akt;
    $("#select_teammate").attr("disabled", "true");
    $("#active_game").css("visibility", "visible");
    $("#select_winner option:contains('Mein Team')").text(window.localStorage.getItem("user") + " " + players[0].name);
    $("#select_winner option:contains('Gegner Team')").text(players[1].name + " " + players[2].name);
}

function onWinnerSelected() {
    let v = $("#select_winner").val();
    if (v == 0) {
        $("#winner").text(i18n.win);
        $("#winner").css({ "color": "green", "font-size": "larger", "font-weight": "bold" });
    } else if (v == 1) {
        $("#winner").text(i18n.lose);
        $("#winner").css({ "color": "red", "font-size": "larger", "font-weight": "bold" });
        
    }
    $("#send_winner").attr("disabled", "false");
}

function switchCamera(){
    if(cams.length !== undefined && camIndex < cams.length - 1){
        camIndex += 1;
    }else{
        camIndex = 0;
    }
    scanner.stop().then(function(){
        scanner = new Instascan.Scanner({ video: document.getElementById('prev'), mirror: false });
        scanner.start(cams[camIndex]).catch(function(){
                //go on to next camera
                //TODO: in case of no camera working -> endless running loop
                switchCamera();
            });
        }
    );
}
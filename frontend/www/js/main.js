function openTab(evt, tabname) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabname).style.display = "block";
    if (evt === null) {
        document.getElementById("tab0").className += " active";
    } else {
        evt.currentTarget.className += " active";
    }


    workOn(tabname, undefined);
}

function workOn(tabname, param) {
    if (tabname === "leaderboard") {
        createConfirmPopup();
        var request = {};
        $.ajax({
            type: "GET",
            url: base_url + "/leaderboard",
            data: request,
            complete: function (response) {
                var players_leaderboard = JSON.parse(response.responseText).leaderboard;
                var leaderboard = document.getElementById("leaderboard_table");
                var child = leaderboard.lastElementChild;
                while (child) {
                    leaderboard.removeChild(child);
                    child = leaderboard.lastElementChild;
                }
                var h = leaderboard.insertRow(-1);
                h.innerHTML = "<th>Nickname</th><th>Score</th>";
                for (var i = 0; i < players_leaderboard.length; i++) {
                    var row = leaderboard.insertRow(-1);
                    var user = row.insertCell(0);
                    var score = row.insertCell(1);
                    user.innerText = players_leaderboard[i].username;
                    score.innerText = players_leaderboard[i].elo;
                    user.className = "name";
                    score.className = "score";
                }
            },
            dataType: "text/json"
        })
        return
    }
    if (tabname === "profile") {

        if (param !== undefined) {
            generateProfile(param)
        } else {
            var profile = {};
            profile.email = window.localStorage.getItem("email");
            profile.user = window.localStorage.getItem("user");
            profile.uuid = window.localStorage.getItem("uuid");
            generateProfile(profile);
        }
    }
}

function generateProfile(profile) {
    cordova.plugins.qrcodejs.encode('TEXT_TYPE', profile.uuid + "[&!?]" + profile.user, (base64EncodedQRImage) => {
        document.getElementById("QRimage").src = base64EncodedQRImage;
        document.getElementById("username_profile").innerText = profile.user;

        if (document.getElementById("email_entry").lastChild !== null) {
            document.getElementById("email_entry").removeChild(document.getElementById("email_entry").lastChild);
        }
        if (profile.email === undefined || profile.email === "undefined" || profile.email === null || profile.email === "") {
            var div = document.createElement('div');
            div.innerHTML = "<input id='input_email' type='email' placeholder='Hinterlege deine Email' class='info'/><br\><input type='button' value='Speichern' id='save_btn' onclick='save()'/>";
            document.getElementById("email_entry").appendChild(div);
        } else {
            var div = document.createElement('div');
            div.innerHTML = "<p id='email_profile' class='info'></p>"
            div.firstChild.innerText = profile.email;
            document.getElementById("email_entry").appendChild(div);
        }
        generate_personal_history();
    }, (err) => {
        console.error('QRCodeJS error is ' + JSON.stringify(err));
    });
}
var players;
function new_game(event, team_size) {
    document.getElementsByTagName("body")[0].className = "body_bg_invisible";
    document.getElementById("start_game").style.visibility = "hidden";
    team_size = team_size * 2 - 1;
    var ids = [];
    try {
        var callback = function (err, text) {
            if (err) {
                throw "Scan error";
            } else {
                var name = text.split("[&!?]")[1];
                var uuid = text.split("[&!?]")[0];
                alert(name);
                //check wether id exists:
                ids.push({ name: name, uuid: uuid });
                if (ids.length === team_size) {
                    display_team(ids, team_size);
                } else {
                    window.QRScanner.scan(callback);
                }
            }
        }
        window.QRScanner.scan(callback);
        window.QRScanner.show();
    } catch (e) {
        document.getElementById("start_game").style.visibility = "visible";
        document.getElementsByTagName("body")[0].className = "body_bg";
    }
}

function display_team(ids, team_size) {
    try {
        window.QRScanner.destroy();
    } catch (e) {
        console.log("QR Reader error: " + e);
    }
    document.getElementsByTagName("body")[0].classList = "body_bg";
    if ((ids.length === team_size) && (team_size === 3)) {
        var teams = document.getElementById("team");
        var div = document.createElement("DIV");
        div.innerText = "Waehle deinen Partner:";
        div.className = "team_ch";
        teams.appendChild(div);

        for (var i = 0; i < ids.length; i++) {
            var div = document.createElement("DIV");
            div.innerText = ids[i].name;
            div.className = "teammember";
            div.onclick = team_choser;
            teams.appendChild(div);
        }
    } else if (ids.length === team_size && team_size === 1) {
        //start game ajax
        players = ids;
        document.getElementById("active_game").style.visibility = "visible";
        document.getElementById("b1").placeholder = window.localStorage.getItem("user");
        document.getElementById("b2").placeholder = ids[0].name;

    }
    return;
}

function send_winner() {
    var game = {};
    ids = players;
    players = undefined;
    game.host = window.localStorage.getItem("uuid");
    if (ids.length === 3) {
        game.friend = ids[0].uuid;
        game.enemy1 = ids[1].uuid;
        game.enemy2 = ids[2].uuid;
        if (document.getElementById("winner").style.color === "green") {
            game.winner = 0;
        } else {
            game.winner = 1;
        }
        $.ajax({
            type: "POST",
            url: base_url + "/match/2v2",
            data: game,
            complete: function (response) {
                console.log(response);
                window.location = "./main.html";
            },
            dataType: "text/json"
        })
    } else {
        game.enemy = ids[0].uuid;
        if (document.getElementById("winner").style.color === "green") {
            game.winner = 0;
        } else {
            game.winner = 1;
        }
        $.ajax({
            type: "POST",
            url: base_url + "/match/1v1",
            data: game,
            complete: function (response) {
                console.log(response);
                window.location = "./main.html";
            },
            dataType: "text/json"
        })
    }
    return;
}

function team_choser(evt) {
    var teammate = [evt.currentTarget.innerText];
    var e = document.getElementById("team");
    var child = e.lastElementChild;
    while (child) {
        if (child.innerText !== teammate[0]) {
            teammate.push(child.innerText);
        }
        e.removeChild(child);
        child = e.lastElementChild;
    }
    //start game ajax
    players = teammate;
    document.getElementById("active_game").style.visibility = "visible";
    document.getElementById("b1").placeholder = window.localStorage.getItem("user") + ", " + ids[0];
    document.getElementById("b2").placeholder = ids[1] + ", " + ids[2];
}

function check_winner() {
    var v1 = document.getElementById("b1").value;
    var v2 = document.getElementById("b2").value;
    if (v1 != 0 && v2 != 0) {
        document.getElementById("winner").innerText = "Einer muss gewinnen und 0 Becher haben ;)";
    } else if (v1 == 0) {
        document.getElementById("winner").innerText = "DU HAST GEWONNEN";
        document.getElementById("winner").style.color = "green";
        document.getElementById("send_winner").disabled = false;
    } else if (v2 == 0) {
        document.getElementById("winner").innerText = "DU HAST VERLOREN";
        document.getElementById("winner").style.color = "red";
        document.getElementById("send_winner").disabled = false;
    }
}

function save() {
    var profile = {};
    profile.username = window.localStorage.getItem("user");
    profile.mail = document.getElementById("input_email").value;
    profile.passwd = window.localStorage.getItem("password");
    $.ajax({
        type: "PUT",
        url: base_url + "/users/mail/update",
        data: profile,
        complete: function (response) {
            if (JSON.parse(response.responseText).status === "mail updated") {
                window.localStorage.setItem("email", profile.mail);
                workOn("profile", undefined);
            }
        }
    });
}

function onLeftSwipe() {
    if (deactivated)
        return
    var tablinks = document.getElementsByClassName("tablinks");
    for (var i = 0; i < tablinks.length; i++) {
        if (tablinks[i].className.includes("active")) {
            if (i == 0) {
                openTab({ currentTarget: tablinks[1] }, "game");
            } else if (i == 1) {
                openTab({ currentTarget: tablinks[2] }, "profile");
            }
            return;
        }
    }
}

function onRightSwipe() {
    if (deactivated)
        return
    var tablinks = document.getElementsByClassName("tablinks");
    for (var i = 0; i < tablinks.length; i++) {
        if (tablinks[i].className.includes("active")) {
            if (i == 1) {
                openTab({ currentTarget: tablinks[0] }, "leaderboard");
            } else if (i == 2) {
                openTab({ currentTarget: tablinks[1] }, "game");
            }
            return;
        }
    }
}

var deactivated = false;
var confirms;

function confirmResults() {
    var request = {}
    request.username = window.localStorage.getItem("user");
    request.passwd = window.localStorage.getItem("password");
    for (var i = 0; i < confirms.length; i++) {
        confirms[i].confirmed = document.getElementById("check" + i).checked;
    }
    request.matches = JSON.stringify(confirms);
    confirms = [];
    $.ajax({
        type: "POST",
        url: base_url + "/match/confirm",
        data: request,
        complete: function (response) {
            console.log("Confirmed");
            document.getElementById("confirmPopup").style.visibility = "hidden";
            document.getElementById("tab0").disabled = false;
            document.getElementById("tab1").disabled = false;
            document.getElementById("tab2").disabled = false;
            deactivated = false;
            workOn("leaderboard", undefined);
        }
    });
}

function createConfirmPopup() {
    var request = {};
    request.userid = window.localStorage.getItem("uuid");
    $.ajax({
        type: "GET",
        url: base_url + "/match/pending",
        data: request,
        complete: function (response) {
            confirms = JSON.parse(response.responseText).matches;
            if (confirms.length !== 0) {
                deactivated = true;
                document.getElementById("confirmPopup").style.visibility = "visible";
                document.getElementById("tab0").disabled = true;
                document.getElementById("tab1").disabled = true;
                document.getElementById("tab2").disabled = true;
                var table = document.getElementById("confirms");
                var child = table.lastElementChild;
                while (child) {
                    table.removeChild(child);
                    child = table.lastElementChild;
                }
                for (var i = 0; i < confirms.length; i++) {
                    var row = table.insertRow(-1);
                    var checker = row.insertCell(0);
                    checker.innerHTML = "<input id='check" + i + "' class='checkResult' type='checkbox' checked='true'/>";
                    var text = row.insertCell(1);
                    if (confirms[i].winner === 0) {
                        text.innerHTML = "<span class='checkResultText' style='font-color:red'>Verloren gegen " + confirms[i].hostname + "</span>";
                    } else {
                        text.innerHTML = "<span class='checkResultText' style='font-color:green'>Gewonnen gegen " + confirms[i].hostname + "</span>";
                    }
                }
            }
        },
        dataType: "text/json"
    })
}

function logout() {
    window.localStorage.setItem("user", "");
    window.localStorage.setItem("password", "");
    window.localStorage.setItem("uuid", "");
    window.localStorage.setItem("email", "");
    window.location = "./index.html";
}

function generate_personal_history() {
    var request = {};
    request.username = window.localStorage.getItem("user");
    request.passwd = window.localStorage.getItem("password");
    $.ajax({
        type: "GET",
        url: base_url + "/users/history",
        data: request,
        complete: function (response) {
            var games = JSON.parse(response.responseText).matches;
            var table = document.getElementById("history");
            var child = table.lastElementChild;
            while (child) {
                table.removeChild(child);
                child = table.lastElementChild;
            }
            for (var i = 0; i < games.length; i++) {
                var game = document.createElement("DIV");
                var text = "";
                if(games[i].enemy2 === "None"){
                    var text = games[i].enemy1;
                }else{
                    var text = games[i].enemy1  + " & " + games[i].enemy2;
                }
                if(games[i].winner = 0){
                    game.innerHTML = "<p class='win'>" + text + "</p>";
                }else{
                    game.innerHTML = "<p class='loss'>" + text + "</p>";
                }
                table.appendChild(game.firstChild);
            }
        }
    });
}
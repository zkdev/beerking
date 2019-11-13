function openTab(evt, tabname) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    $("#" + tabname).css("display", "block");
    if (evt === null) {
        $("#tab0").attr("class", "tablinks active");
    } else {
        evt.currentTarget.className += " active";
    }


    workOn(tabname, undefined);
}

function workOn(tabname, param) {
    if (tabname === "leaderboard") {
        createConfirmPopup();
        createLeaderboard();
    }
    if (tabname === "profile") {

        if (param !== undefined) {
            generateProfile(param)
        } else {
            var profile = {
                email: window.localStorage.getItem("email"),
                user: window.localStorage.getItem("user"),
                uuid: window.localStorage.getItem("uuid")
            };
            generateProfile(profile);
        }
    }
    if (tabname === "friends") {
        createFriendsList();
    }
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
            } else if (i == 2) {
                openTab({ currentTarget: tablinks[3] }, "friends");
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
            } else if (i == 3) {
                openTab({ currentTarget: tablinks[2] }, "profile");
            }
            return;
        }
    }
}

var deactivated = false;
var confirms;

function confirmResults() {
    for (var i = 0; i < confirms.length; i++) {
        confirms[i].confirmed = document.getElementById("check" + i).checked;
    }
    var request = {
        username: window.localStorage.getItem("user"),
        passwd: window.localStorage.getItem("password"),
        matches: JSON.stringify(confirms)
    }
    confirms = [];
    SpinnerPlugin.activityStart(i18n.send_accept, options);
    $.ajax({
        type: "POST",
        url: base_url + "/match/confirm",
        data: request,
        complete: function (response) {
            SpinnerPlugin.activityStop();
            $("#confirmPopup").css("visibility", "hidden");
            $("#tab0").attr("disabled", "false");
            $("#tab1").attr("disabled", "false");
            $("#tab2").attr("disabled", "false");
            $("#tab3").attr("disabled", "false");
            deactivated = false;
            workOn("leaderboard", undefined);
        }
    });
}

function createConfirmPopup() {
    var request = {
        userid: window.localStorage.getItem("uuid")
    };
    $.ajax({
        type: "GET",
        url: base_url + "/match/pending",
        data: request,
        complete: function (response) {
            confirms = JSON.parse(response.responseText).matches;
            if (confirms.length !== 0) {
                deactivated = true;
                $("#confirmPopup").css("visibility", "visible");
                $("#tab0").attr("disabled", "true");
                $("#tab1").attr("disabled", "true");
                $("#tab2").attr("disabled", "true");
                $("#tab3").attr("disabled", "true");
                var table = document.getElementById("confirms");
                var child = table.lastElementChild;
                while (child) {
                    table.removeChild(child);
                    child = table.lastElementChild;
                }
                for (let i = 0; i < confirms.length; i++) {
                    var row = table.insertRow(-1);
                    var checker = row.insertCell(0);
                    checker.innerHTML = "<label class='switch'><input id='check" + i + "' class='checkResult' type='checkbox' checked='true'/><span class='slider round'></span></label>";
                    var text = row.insertCell(1);
                    if (confirms[i].winner === 0) {
                        text.innerHTML = "<span class='checkResultText'>Verloren gegen " + confirms[i].hostname + "</span>";
                    } else {
                        text.innerHTML = "<span class='checkResultText'>Gewonnen gegen " + confirms[i].hostname + "</span>";
                    }
                }
            }
        },
        dataType: "text/json"
    })
}

function createLeaderboard() {
    var request = {
        userid: window.localStorage.getItem("uuid")
    }
    $.ajax({
        type: "GET",
        url: base_url + "/leaderboard",
        data: request,
        complete: function (response) {
            var name = window.localStorage.getItem("user");
            var ind = 0;
            document.getElementById("loader_leaderboard").style.display = "none";
            var players_leaderboard = JSON.parse(response.responseText).leaderboard;
            var leaderboard = document.getElementById("leaderboard_table");
            var leaderboard_top = document.getElementById("leaderboard_header");
            var child = leaderboard_top.lastElementChild;
            while (child) {
                leaderboard_top.removeChild(child);
                child = leaderboard_top.lastElementChild;
            }
            var head = leaderboard_top.insertRow(-1);
            head.innerHTML = "<th>Platz</th><th>Nickname</th><th>Score</th>";
            var child = leaderboard.lastElementChild;
            while (child) {
                leaderboard.removeChild(child);
                child = leaderboard.lastElementChild;
            }
            let place = 1;
            for (var i = 0; i < players_leaderboard.length; i++) {
                if(players_leaderboard[i].display === true){
                    var row;
                    if (i < 3) {
                        row = leaderboard_top.insertRow(-1);
                    } else {
                        row = leaderboard.insertRow(-1);
                    }
                    if (i == 0) {
                        row.className = "first";
                    } else if (i == 1) {
                        row.className = "second";
                    } else if (i == 2) {
                        row.className = "third";
                    }
                    if ((i + 1) % 2 == 0) {
                        row.className += " other";
                    }
                    if (players_leaderboard[i].username === window.localStorage.getItem("user")) {
                        row.className += " ich";
                    }
                    if (players_leaderboard[i].isfriend === true) {
                        row.className += " friends";
                    }
                    var nr = row.insertCell(0);
                    nr.innerText = "" + place;
                    place += 1;
                    var user = row.insertCell(1);
                    var score = row.insertCell(2);
                    user.innerText = players_leaderboard[i].username;
                    score.innerText = players_leaderboard[i].elo;
                    user.className = "name"; score.className = "score"; nr.className = "platz";
                    if (i > 2 && name === players_leaderboard[i].username) {
                        ind = i;
                    }
                }
            }
            var rows = leaderboard.querySelectorAll('tr');
            rows[ind - 3].scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        },
        dataType: "text/json"
    });
}

function backToGame() {
    window.location = './main.html';
}

function share(content) {
    navigator.share(content, i18n.share_header, "text/plain");
}
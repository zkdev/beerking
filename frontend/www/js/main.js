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
        var request = {};
        request.password = window.localStorage.getItem("password");
        request.user = window.localStorage.getItem("user");
        $.ajax({
            type: "GET",
            url: base_url + "leaderboard",
            data: request,
            success: function (response) {
                for (var i = 0; i < response.length; i++) {
                    // TODO
                    //append elements response[i]
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
            /**var request = {};
            request.password = window.localStorage.getItem("password");
            request.user = window.localStorage.getItem("user");
            $.ajax({
                type: "GET",
                url: base_url + "profile",
                data: request,
                success: function (response) {
                    // TODO 
                },
                dataType: "text/json"
            })*/
            var profile = {}
            profile.user = "ICH";
            profile.email = "ICH";
            generateProfile(profile);
        }
    }
}

function generateProfile(profile) {
    cordova.plugins.qrcodejs.encode('TEXT_TYPE', profile.user, (base64EncodedQRImage) => {
        document.getElementById("QRimage").src = base64EncodedQRImage;
        document.getElementById("username_profile").innerText = profile.user;

        if (document.getElementById("email_entry").lastChild !== null) {
            document.getElementById("email_entry").removeChild(document.getElementById("email_entry").lastChild);
        }
        if (profile.email === undefined) {
            var div = document.createElement('div');
            div.innerHTML = "<input id='input_email' type='email' placeholder='Hinterlege deine Email' class='info'/><br\><input type='button' value='Speichern' id='save_btn' onclick='save()'/>";
            document.getElementById("email_entry").appendChild(div);
        } else {
            var div = document.createElement('div');
            div.innerHTML = "<p id='email_profile' class='info'></p>"
            div.firstChild.innerText = profile.email;
            document.getElementById("email_entry").appendChild(div);
        }

    }, (err) => {
        console.error('QRCodeJS error is ' + JSON.stringify(err));
    });
}

function new_game(event, team_size) {
    document.getElementsByTagName("body")[0].style.opacity = 0.0;
    document.getElementsByTagName("body")[0].style.background = "transparent";
    document.getElementById("start_game").style.visibility = "hidden";
    team_size = team_size * 2 - 1;
    var ids = [];
    try {
        var callback = function (err, text) {
            if (err) {
                throw "Scan error";
            } else {
                alert(text);
                ids.push(text);
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
        document.getElementsByTagName("body")[0].style.opacity = 1.0;
        document.getElementsByTagName("body")[0].style.background = "url('./../www/img/wood.png')";
        document.getElementsByTagName("body")[0].style.backgroundColor = "white";
        return;
    }
}

function display_team(ids, team_size) {
    try{
        window.QRScanner.destroy();
    }catch(e){}
    document.getElementsByTagName("body")[0].style.opacity = 1.0;
    document.getElementsByTagName("body")[0].style.background = "url('./../www/img/wood.png')";
    document.getElementsByTagName("body")[0].style.backgroundColor = "white";
    if ((ids.length === team_size) && (team_size === 3)) {
        var teams = document.getElementById("team");
        var div = document.createElement("DIV");
        div.innerText = "Waehle deinen Partner:";
        div.className = "team_ch";
        teams.appendChild(div);

        for (var i = 0; i < ids.length; i++) {
            var div = document.createElement("DIV");
            div.innerText = ids[i];
            div.className = "teammember";
            div.onclick = team_choser;
            teams.appendChild(div);
        }
    } else if (ids.length === team_size && team_size === 1) {
        document.getElementById("active_game").style.visibility = "visible";
    }
    return;
}

function team_choser(evt) {
    var teammate = evt.currentTarget.innerText;
    var e = document.getElementById("team");
    var child = e.lastElementChild;
    while (child) {
        e.removeChild(child);
        child = e.lastElementChild;
    }
    document.getElementById("active_game").style.visibility = "visible";
}

function check_winner() {
    var v1 = document.getElementById("b1").value;
    var v2 = document.getElementById("b2").value;
    if (v1 != 0 && v2 != 0) {
        document.getElementById("winner").innerText = "Einer muss gewinnen und 0 Becher haben ;)";
    } else if (v1 == 0) {
        document.getElementById("winner").innerText = "DU HAST GEWONNEN";
        document.getElementById("winner").style.color = "green";
    } else if (v2 == 0) {
        document.getElementById("winner").innerText = "DU HAST VERLOREN";
        document.getElementById("winner").style.color = "red";
    }
}

function save() {
    var profile = {};
    profile.user = document.getElementById("username_profile").innerText;
    profile.email = document.getElementById("input_email").value;
    profile.qrcode = document.getElementById("QRimage").src;
    //ajax call for saving
    workOn("profile", profile);
}
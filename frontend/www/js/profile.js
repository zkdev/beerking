function generateProfile(profile) {
    cordova.plugins.qrcodejs.encode('TEXT_TYPE', profile.uuid + "[&!?]" + profile.user, function(base64EncodedQRImage){
        document.getElementById("QRimage").src = base64EncodedQRImage;
        document.getElementById("username_profile").innerText = profile.user;

        if (document.getElementById("email_entry").lastChild !== null) {
            document.getElementById("email_entry").removeChild(document.getElementById("email_entry").lastChild);
        }
        if(profile.mail === null || profile.mail === undefined){
            profile.mail = "";
        }
        var div = document.createElement('div');
        div.innerHTML = "<input id='input_email' type='email' placeholder='Hinterlege deine Email' class='info' value='" + profile.email + "'/><input type='button' value='Speichern' id='save_btn' class='btn_style' onclick='save()'/>";
        document.getElementById("email_entry").appendChild(div);
        
        gerneratePersonalHistory();
    }, function(err){
        console.error('QRCodeJS error is ' + JSON.stringify(err));
    });
}

function save() {
    var profile = {};
    profile.username = window.localStorage.getItem("user");
    profile.mail = document.getElementById("input_email").value;
    profile.passwd = window.localStorage.getItem("password");
    SpinnerPlugin.activityStart("Speichern...", options);
    $.ajax({
        type: "PUT",
        url: base_url + "/user/mail/update",
        data: profile,
        complete: function(response) {
            SpinnerPlugin.activityStop();
            if (JSON.parse(response.responseText).mail_updated === true) {
                window.localStorage.setItem("email", profile.mail);
                workOn("profile", undefined);
            }else{
                navigator.notification.alert("Diese Email existiert nicht", null, "Fehler");
                workOn("profile", undefined);
            }
        }
    });
}

function gerneratePersonalHistory() {
    var request = {};
    request.username = window.localStorage.getItem("user");
    request.passwd = window.localStorage.getItem("password");
    $.ajax({
        type: "GET",
        url: base_url + "/user/history",
        data: request,
        complete: function(response) {
            function formatString(date) {
                function double(min) {
                    if (min < 10) {
                        return "0" + min;
                    } else {
                        return "" + min;
                    }
                }
                return "" + double(date.getDate()) + "." + double(date.getMonth() + 1) + " " + double(date.getHours()) + ":" + double(date.getMinutes());
            }
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
                var user = window.localStorage.getItem("user");
                if (games[i].friend === user || games[i].host === user) {
                    var text = formatString(new Date(games[i].datetime)) + " : ";
                    if (games[i].enemy2 === null) {
                        text += games[i].enemy1;
                    } else {
                        text += games[i].enemy1 + " & " + games[i].enemy2;
                    }
                    if (games[i].winner === 0) {
                        game.innerHTML = "<p class='win'>" + text + "</p>";
                    } else {
                        game.innerHTML = "<p class='loss'>" + text + "</p>";
                    }
                } else {
                    var text = formatString(new Date(games[i].datetime)) + " : ";
                    if (games[i].friend === null) {
                        text += games[i].host;
                    } else {
                        text += games[i].host + " & " + games[i].friend;
                    }
                    if (games[i].winner === 1) {
                        game.innerHTML = "<p class='win'>" + text + "</p>";
                    } else {
                        game.innerHTML = "<p class='loss'>" + text + "</p>";
                    }
                }
                table.appendChild(game.firstChild);
            }
        }
    });
}

function logout() {
    window.localStorage.setItem("user", "");
    window.localStorage.setItem("password", "");
    window.localStorage.setItem("uuid", "");
    window.localStorage.setItem("email", "");
    window.location = "./index.html";
}
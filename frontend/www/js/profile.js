function generateProfile(profile) {
    cordova.plugins.qrcodejs.encode('TEXT_TYPE', profile.uuid + "[&!?]" + profile.user, function (base64EncodedQRImage) {
        $("#QRimage").attr("src", base64EncodedQRImage);
        $("#username_profile").text(profile.user);

        if (document.getElementById("email_entry").lastChild !== null) {
            document.getElementById("email_entry").removeChild(document.getElementById("email_entry").lastChild);
        }
        if (profile.mail === null || profile.mail === undefined) {
            profile.mail = "";
        }
        var div = document.createElement('div');
        div.innerHTML = "<input id='input_email' type='email' placeholder='Hinterlege deine Email' class='info' value='" + profile.email + "'/><input type='button' value='Speichern' id='save_btn' class='btn_style' onclick='save()'/>";
        document.getElementById("email_entry").appendChild(div);

        gerneratePersonalHistory();
    }, function (err) { });
}

function save() {
    var profile = {
        username: window.localStorage.getItem("user"),
        mail: $("#input_email").val(),
        passwd: window.localStorage.getItem("password")
    };

    SpinnerPlugin.activityStart(i18n.save, options);
    $.ajax({
        type: "PUT",
        url: base_url + "/user/mail/update",
        data: profile,
        complete: function (response) {
            SpinnerPlugin.activityStop();
            if (JSON.parse(response.responseText).mail_updated === true) {
                window.localStorage.setItem("email", profile.mail);
                workOn("profile", undefined);
            } else {
                navigator.notification.alert(i18n.profile_not_existing_mail, null, i18n.login_alert_button);
                workOn("profile", undefined);
            }
        }
    });
}

function gerneratePersonalHistory() {
    var request = {
        username: window.localStorage.getItem("user"),
        passwd: window.localStorage.getItem("password")
    }
    $.ajax({
        type: "GET",
        url: base_url + "/user/history",
        data: request,
        complete: function (response) {
            function formatString(date) {
                function double(min) {
                    return (min < 10) ? ("0" + min) : ("" + min);
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
            for (let i = 0; i < games.length; i++) {
                var game = document.createElement("DIV");
                var user = window.localStorage.getItem("user");
                if (games[i].friend === user || games[i].host === user) {
                    let text = formatString(new Date(games[i].datetime.replace(/-/g, "/"))) + " : ";
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
                    let text = formatString(new Date(games[i].datetime.replace(/-/g, "/"))) + " : ";
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
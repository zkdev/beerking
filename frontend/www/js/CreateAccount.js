function createAccount() {
    var account_setting = {};
    account_setting.passwd = hash(document.getElementById("pswd").value);
    if (document.getElementById("pswd").value === "" || document.getElementById("user").value === "") {
        //No user or password
        navigator.notification.alert("Nutzer und Passwort muessen ausgefuellt werden", null, "Falsche Eingabe", "Ok");
        document.getElementById("pswd").value = "";
        document.getElementById("pswd2").value = "";
        return;
    }
    if(document.getElementById("user").value.trim().includes(";") || document.getElementById("user").value.trim().includes("'") || document.getElementById("user").value.trim().includes("%") || document.getElementById("user").value.trim().includes("--")){
        navigator.notification.alert("Der Nickname darf keines der folgenden Zeichen erhalten: ; ' -- %", null, "Nicht erlaubte Eingabe", "Ok")
        document.getElementById("user").value = "";
        return;
    }

    if (hash(document.getElementById("pswd2").value) !== account_setting.passwd) {
        //Different passwords
        document.getElementById("pswd2").className += " error";
        document.getElementById("pswd").className += " error";
        document.getElementById("pswd").value = "";
        document.getElementById("pswd2").value = "";
        navigator.notification.alert("Passwoerter mussen identisch sein!", null, "Falsche Eingabe", "Ok");
        return;
    }
    account_setting.username = document.getElementById("user").value.trim();
    account_setting.mail = document.getElementById("email").value;
    SpinnerPlugin.activityStart("Account erstellen...", options);
    $.ajax({
        type: "POST",
        url: base_url + "/user/create",
        data: account_setting,
        complete: function(response) {
            SpinnerPlugin.activityStop();
            var resp = JSON.parse(response.responseText);
            if (resp.user_created === true) {
                window.localStorage.setItem("password", account_setting.passwd);
                window.localStorage.setItem("user", account_setting.username);
                window.location = './index.html';
            } else {
                if(resp.username_unique !== true){
                    navigator.notification.alert("Deinen Nickname gibt es leider schon!", null, "Fehler", "Ok");
                    window.location = "./creating.html";
                    return;
                }
                if(resp.username_too_short === true){
                    navigator.notification.alert("Dein Nickname ist zu kurz (mindestens 3 Zeichen)", null, "Fehler", "Ok");
                    window.location = "./creating.html";
                    return;
                }
                if(resp.mail_exists !== false){
                    navigator.notification.alert("Die Email existiert nicht, gib keine oder eine existierende Email an", null, "Fehler", "Ok");
                    window.location = "./creating.html";
                    return;
                }
            }
        },
        dataType: "text/json"
    });
}
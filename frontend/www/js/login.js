function onLogin() {
    //Summit login values
    var login_values = {};
    login_values.passwd = hash(document.getElementById("pswd").value);
    login_values.username = document.getElementById("user").value.trim();

    SpinnerPlugin.activityStart("Einloggen...", options);
    $.ajax({
        type: "GET",
        url: base_url + "/user/profile",
        data: login_values,
        complete: function(response) {
            SpinnerPlugin.activityStop();
            var resp = "";
            try {
                resp = JSON.parse(response.responseText);
            } catch (e) {}
            if (resp.auth === true) {
                window.localStorage.setItem("password", login_values.passwd);
                window.localStorage.setItem("user", login_values.username);
                window.localStorage.setItem("uuid", resp.userid);
                window.localStorage.setItem("email", resp.mail);
                window.location = './main.html';
            } else {
                // wrong email / wrong username
                if(resp.status === "" || resp.status === null || resp.status === undefined || resp.status.startsWith('<')){
                    resp.status = "Server gerade nicht erreichbar, versuchen sie es spaeter erneut oder laden sie die neuste Version aus dem Appstore herunter";
                }
                navigator.notification.alert(resp.status, null, "Login fehlgeschlagen", "Ok");
                document.getElementById("pswd").value = "";
                document.getElementById("user").value = "";

            }
        },
        dataType: "text/json"
    })
}
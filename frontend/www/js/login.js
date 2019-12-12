function onLogin() {
    //Summit login values
    let login_values = {
        passwd: hash($("#pswd").val()),
        username: $("#user").val().trim()
    }

    SpinnerPlugin.activityStart(i18n.login_message, options);
    $.ajax({
        type: "GET",
        url: base_url + "/user/profile",
        data: login_values,
        complete: function (response) {
            SpinnerPlugin.activityStop();
            try {
                var resp = JSON.parse(response.responseText);
            } catch (e) { }
            if (resp && resp.auth === true) {
                window.localStorage.setItem("password", login_values.passwd);
                window.localStorage.setItem("user", login_values.username);
                window.localStorage.setItem("uuid", resp.userid);
                window.localStorage.setItem("email", resp.mail);
                window.location = './main.html';
            } else {
                // wrong email / wrong username
                if (!resp || resp.status === "" || resp.status === null || resp.status === undefined || resp.status.startsWith('<')) {
                    navigator.notification.alert(i18n.login_alert_standard_message, null, i18n.login_alert_heading, i18n.login_alert_button);
                } else {
                    navigator.notification.alert(resp.status, i18n.login_alert_heading, i18n.login_alert_button);
                }
                $("#pswd").val("");
                $("#user").val("");
            }
        },
        dataType: "text/json"
    })
}
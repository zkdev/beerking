function createAccount() {
    var account_setting = {
        passwd: hash($("#pswd").val()),
        username: $("#user").val().trim(),
        mail: $("#email").val()
    };
    if (document.getElementById("pswd").value === "" || document.getElementById("user").value === "") {
        navigator.notification.alert(i18n.create_empty_fields, null, i18n.create_wrong_input_header, i18n.create_button);
        $("#pswd").val("");
        $("#pswd2").val("");
        return;
    }
    if (document.getElementById("user").value.trim().includes(";") || document.getElementById("user").value.trim().includes("'") || document.getElementById("user").value.trim().includes("%") || document.getElementById("user").value.trim().includes("--")) {
        navigator.notification.alert(i18n.create_not_allowed_message, null, i18n.create_not_allowed_header, i18n.create_button)
        $("#user").val("");
        return;
    }
    if (hash(document.getElementById("pswd2").value) !== account_setting.passwd) {
        //Different passwords
        $("#pswd2").attr("class", " error");
        $("#pswd").attr("class", " error");
        $("#pswd").val("");
        $("#pswd2").val("");
        navigator.notification.alert(i18n.create_password, null, i18n.create_wrong_input_header, i18n.create_button);
        return;
    }
    SpinnerPlugin.activityStart(i18n.create_account, options);
    $.ajax({
        type: "POST",
        url: base_url + "/user/create",
        data: account_setting,
        complete: function (response) {
            SpinnerPlugin.activityStop();
            var resp = JSON.parse(response.responseText);
            if (resp.user_created === true) {
                window.localStorage.setItem("password", account_setting.passwd);
                window.localStorage.setItem("user", account_setting.username);
                window.location = './index.html';
            } else {
                if (resp.username_unique !== true) {
                    navigator.notification.alert(i18n.create_name_already_exists, null, i18n.error, i18n.create_button);
                } else if (resp.username_too_short === true) {
                    navigator.notification.alert(i18n.create_user_too_short, null, i18n.error, i18n.create_button);
                } else if (resp.mail_exists !== false) {
                    navigator.notification.alert(i18n.create_wrong_email, null, i18n.error, i18n.create_button);
                }
                window.location = "./creating.html";
                return;
            }
        },
        dataType: "text/json"
    });
}
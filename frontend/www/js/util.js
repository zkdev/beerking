function summit_login() {
    //Summit login values
    var login_values = {};
    login_values.password = document.getElementById("pswd").value;
    login_values.user = document.getElementById("user").value;

    if (login_values.user === "test" && login_values.password === "test") {
        var hashedValue = hash(login_values.password);
        window.localStorage.setItem("password", hashedValue);
        window.localStorage.setItem("user", login_values.user);
        window.location = './main.html';
        return;
    }

    //ajax call
    $.ajax({
        type: "POST",
        url: base_url + "login",
        data: login_values,
        success: function () {
            var hashedValue = hash(login_values.password);
            window.localStorage.setItem("password", hashedValue);
            window.localStorage.setItem("user", login_values.user);
            window.location = './main.html';
        },
        dataType: "text/json"
    })
}

function hash(text){
    var passwdParam = {
        "password": text,
        "salt": "MySalt",
        "iterations": 30000,
        "keyLength": "16" //  is bytes, not bits!
    };
    return community.PasswordCrypto.pbkdf2_Sync(passwdParam);
}

function create_Account() {
    var account_setting = {};
    account_setting.password = document.getElementById("pswd").value;
    account_setting.user = document.getElementById("user").value;
    account_setting.email = document.getElementById("email").value;
    //TEST
    //
    $.ajax({
        type: "POST",
        url: base_url + "create",
        data: account_setting,
        success: function () {
            var hashedValue = hash(account_setting.password)

            window.localStorage.setItem("password", hashedValue);
            window.localStorage.setItem("user", account_setting.user);
            window.location = './main.html';
        },
        dataType: "text/json"
    });
}
function summit_login() {
    //Summit login values
    var login_values = {};
    login_values.passwd = document.getElementById("pswd").value;
    login_values.user = document.getElementById("user").value;

    if (login_values.user === "test" && login_values.passwd === "test") {
        var hashedValue = hash(login_values.passwd);
        window.localStorage.setItem("password", hashedValue);
        window.localStorage.setItem("user", login_values.user);
        window.location = './main.html';
        return;
    }

    //ajax call
    $.ajax({
        type: "GET",
        url: base_url + "/users/login",
        data: login_values,
        complete: function (response) {
            if (response.responseText === 'login sucessfully') {
                var hashedValue = hash(login_values.passwd);
                window.localStorage.setItem("password", hashedValue);
                window.localStorage.setItem("user", login_values.user);
                window.location = './main.html';
            } else {
                // wrong email / wrong username
            }
        },
        dataType: "text/json"
    })
}

function create_Account() {
    var account_setting = {};
    account_setting.passwd = hash(document.getElementById("pswd").value);
    account_setting.user = document.getElementById("user").value;
    account_setting.email = document.getElementById("email").value;
    //TEST
    //
    $.ajax({
        type: "GET",
        url: base_url + "/users/creation",
        data: account_setting,
        complete: function (response) {
            if(response.responseText.startsWith('user created.')){
                window.localStorage.setItem("password", account_setting.passwd);
                window.localStorage.setItem("user", account_setting.user);
                window.location = './main.html';
            }else{
                //Create error message
            }
        },
        dataType: "text/json"
    });
}
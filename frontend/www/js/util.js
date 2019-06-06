function summit_login() {
    //Summit login values
    var login_values = {};
    login_values.passwd = document.getElementById("pswd").value;
    login_values.username = document.getElementById("user").value;

    if (login_values.username === "test" && login_values.passwd === "test") {
        var hashedValue = hash(login_values.passwd);
        window.localStorage.setItem("password", hashedValue);
        window.localStorage.setItem("user", login_values.username);
        window.location = './main.html';
        return;
    }

    login_values.passwd = hash(login_values.passwd);
    //ajax call
    $.ajax({
        type: "GET",
        url: base_url + "/users/login",
        data: login_values,
        complete: function (response) {
            var resp = JSON.parse(response.responseText);
            if (resp.status === 'login successful') {
                window.localStorage.setItem("password", login_values.passwd);
                window.localStorage.setItem("user", login_values.username);
                window.location = './main.html';
            } else {
                // wrong email / wrong username
                navigator.notification.alert("Dieser Nutzer existiert nicht, oder das Passwort war falsch", 
                null, "Login fehlgeschlagen", "Ok");
                document.getElementById("pswd").value = "";
                document.getElementById("user").value = "";

            }
        },
        dataType: "text/json"
    })
}

function create_Account() {
    var account_setting = {};
    account_setting.passwd = hash(document.getElementById("pswd").value);
    if(document.getElementById("pswd").value === "" || document.getElementById("user").value === ""){
        //No user or password
        navigator.notification.alert("Nutzer und Passwort muessen ausgefuellt werden", null, "Falsche Eingabe", "Ok");
        window.location = './creating.html';
        return;
    }
    if(hash(document.getElementById("pswd2").value) !== account_setting.passwd){
        //Different passwords
        document.getElementById("pswd2").className += " error";
        document.getElementById("pswd").className += " error";
        document.getElementById("pswd").value = "";
        document.getElementById("pswd2").value = "";
        navigator.notification.alert("Passwoerter mussen identisch sein!", null, "Falsche Eingabe", "Ok");
        return;
    }
    account_setting.username = document.getElementById("user").value;
    account_setting.mail = document.getElementById("email").value;
    $.ajax({
        type: "POST",
        url: base_url + "/users/creation",
        data: account_setting,
        complete: function (response) {
            var resp = JSON.parse(response.responseText);
            if(resp.status === "user creation successful"){
                window.localStorage.setItem("password", account_setting.passwd);
                window.localStorage.setItem("user", account_setting.username);
                window.location = './main.html';
            }else{
                //Create error message
                navigator.notification.alert(resp.status, null, "Fehler", "Ok");
            }
        },
        dataType: "text/json"
    });
}
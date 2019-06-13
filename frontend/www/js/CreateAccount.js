function createAccount() {
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
    account_setting.username = document.getElementById("user").value.trim();
    account_setting.mail = document.getElementById("email").value;
    SpinnerPlugin.activityStart("Account erstellen...", options);
    $.ajax({
        type: "POST",
        url: base_url + "/users/creation",
        data: account_setting,
        complete: function (response) {
            SpinnerPlugin.activityStop();
            var resp = JSON.parse(response.responseText);
            if(resp.status === "user creation successful"){
                window.localStorage.setItem("password", account_setting.passwd);
                window.localStorage.setItem("user", account_setting.username);
                window.location = './index.html';
            }else{
                //Create error message
                navigator.notification.alert(resp.status, null, "Fehler", "Ok");
            }
        },
        dataType: "text/json"
    });
}
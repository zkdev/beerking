/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
var port = 5000;
var base_url = "https://shared.zeggiedieziege.de:" + port;
var options = { dimBackground: true };
var version = 130;

$.ajaxSetup({
    beforeSend: function(xhr) {
        xhr.setRequestHeader("version", version);
    }
});

var app = {
    // Application Constructor
    initialize: function(env) {
        if (env === 'index') {
            document.addEventListener('deviceready', this.onDeviceReady.bind(this), false);
            $(document).on('keypress', keyLogin);
        } else if (env === 'main') {
            document.addEventListener('backbutton', onBackPressed, false);
        }
    },
    onDeviceReady: function() {
        let user = {
            username: window.localStorage.getItem("user"),
            passwd : window.localStorage.getItem("password")
        };
        try {
            if (user.passwd !== undefined && user.passwd !== "") {
                SpinnerPlugin.activityStart(i18n.login_message, options);
                $.ajax({
                    type: "GET",
                    url: base_url + "/user/profile",
                    data: user,
                    complete: function(response) {
                        SpinnerPlugin.activityStop();
                        let resp = JSON.parse(response.responseText);
                        if (resp.auth === true) {
                            window.localStorage.setItem("uuid", resp.userid);
                            window.localStorage.setItem("email", resp.mail);
                            window.location = './main.html';
                        }
                    },
                    dataType: "text/json"
                });
            }
        } catch (e) {}
    }
};

function hash(text) {
    return md5(text);

}

function onBackPressed() {
    //if scanner active -> close
    if($("#prev").attr("class") === "active")
            window.location = "./main.html";
}

function keyLogin(e) {
    if (e.keyCode  == 13) {
        onLogin();
    }
}

var i18n = {
    login_alert_heading : "Login fehlgeschlagen",
    login_alert_standard_message : "Server gerade nicht erreichbar, versuchen sie es spaeter erneut oder laden sie die neuste Version aus dem Appstore herunter",
    login_alert_button : "Ok",
    login_message : "Einloggen...",

    check_spieler_message : "Checke Spieler...",
    player_scanned_header : "Spieler gescannt",
    chose_teammate : "Wähle deinen Partner:",
    choose : "Wählen",

    send_winner : "Schicke Gewinner...",
    win : "DU HAST GEWONNEN",
    lose : "DU HAST VERLOREN",
    
    friend_remove : "Freund entfernen...",
    friend_add : "Freund entfernen...",
    
    create_empty_fields : "Nutzer und Passwort muessen ausgefuellt werden",
    create_wrong_input_header : "Falsche Eingabe",
    create_not_allowed_header : "Nicht erlaubte Eingabe",
    create_not_allowed_message : "Der Nickname darf keines der folgenden Zeichen erhalten: ; ' -- %",
    create_button : "Ok",
    create_password : "Passwoerter mussen identisch sein!",
    create_account : "Account erstellen...",
    error : "Fehler",
    create_name_already_exists : "Deinen Nickname gibt es leider schon!",
    create_user_too_short : "Dein Nickname ist zu kurz (mindestens 3 Zeichen)",
    create_wrong_email : "Die Email existiert nicht, gib keine oder eine existierende Email an",
    
    send_accept : "Schicke Bestaetigungen...",
    share_header : "Teile das Beerking-Erlebnis",
    save : "Speichern...",
    profile_not_existing_mail : "Diese Email existiert nicht"
}
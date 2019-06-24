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
var port = 7000;
var base_url = "http://zeggiedieziege.de:" + port;
var options = { dimBackground: true };
var version = 120;

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
        var user = {};
        try {
            user.username = window.localStorage.getItem("user");
            user.passwd = window.localStorage.getItem("password");
            if (user.passwd !== undefined && user.passwd !== "") {
                SpinnerPlugin.activityStart("Logging in...", options);
                $.ajax({
                    type: "GET",
                    url: base_url + "/user/profile",
                    data: user,
                    complete: function(response) {
                        SpinnerPlugin.activityStop();
                        var resp = JSON.parse(response.responseText);
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
    window.QRScanner.getStatus(function(status){
        if (status.scanning === true) {
            window.QRScanner.cancelScan();
            window.location = "./main.html";
        }
    })
}

function keyLogin(e) {
    if (e.keyCode  == 13) {
        onLogin();
    }
}
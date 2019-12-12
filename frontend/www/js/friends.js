function createFriendsList() {
    var table = document.getElementById("friend_list");
    var child = table.lastElementChild;
    while (child) {
        table.removeChild(child);
        child = table.lastElementChild;
    }
    var request = {
        userid: window.localStorage.getItem("uuid")
    };
    $.ajax({
        type: "GET",
        url: base_url + "/friends",
        data: request,
        complete: function (response) {
            var friends = JSON.parse(response.responseText).friends;
            for (var i = 0; i < friends.length; i++) {
                var fr = document.createElement("DIV");
                fr.className = "friend";
                fr.innerHTML = "<span class='friend_name'>" + friends[i].friendname + "</span><img onclick='deleteFriend(this)' src='./img/del.png' height='20px' width='20px' name='" + friends[i].friendname + "' class='del_item'/>";
                table.appendChild(fr);
            }
        }
    });
}

function addFriend() {
    var request = {
        userid: window.localStorage.getItem("uuid"),
        friendname: $("#username").val().trim()
    }
    SpinnerPlugin.activityStart(i18n.friend_add, options);
    $.ajax({
        type: "POST",
        url: base_url + "/friends/add",
        data: request,
        complete: function () {
            SpinnerPlugin.activityStop();
            $("#username").val("");
            createFriendsList();
        }
    });
}

function deleteFriend(evt) {
    var request = {
        userid: window.localStorage.getItem("uuid"),
        friendname: evt.name
    }
    SpinnerPlugin.activityStart(i18n.friend_remove, options);
    $.ajax({
        type: "DELETE",
        url: base_url + "/friends/remove",
        data: request,
        complete: function () {
            SpinnerPlugin.activityStop();
            createFriendsList();
        }
    });
}
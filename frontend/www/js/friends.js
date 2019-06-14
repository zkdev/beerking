function createFriendsList() {
    var table = document.getElementById("friend_list");
    var child = table.lastElementChild;
    while (child) {
        table.removeChild(child);
        child = table.lastElementChild;
    }
    var request = {};
    request.userid = window.localStorage.getItem("uuid");
    $.ajax({
        type: "GET",
        url: base_url + "/friends",
        data: request,
        complete: function (response) {
            var friends = JSON.parse(response.responseText).friends;
            for (var i = 0; i < friends.length; i++) {
                var fr = document.createElement("DIV");
                fr.className = "friend";
                fr.innerHTML = "<span class='friend_name'>" + friends[i].friendname + "</span><img onclick='deleteFriend()' src='./img/del.png' height='20px' width='20px' class='del_item'/>";
                table.appendChild(fr);
            }
        }
    });
}

function addFriend() {
    var request = {};
    request.userid = window.localStorage.getItem("uuid");
    request.friendname = document.getElementById("username").value;
    $.ajax({
        type: "POST",
        url: base_url + "/friends/add",
        data: request,
        complete: function () {
            createFriendsList();
        }
    });
}

function deleteFriend(evt){
    console.log(evt);
}
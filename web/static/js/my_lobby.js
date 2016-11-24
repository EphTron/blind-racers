// Copyright 2009 FriendFeed
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License. You may obtain
// a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations
// under the License.
var players = [];

class Player {
  constructor(id, name, state) {
    console.log("id:", id, "name:", name)
    this.id = id;
    this.name = name;
    this.state = state;
    console.log("created player", this)
  }

  changeState(new_state){
    this.state = new_state;
  }
}

$(document).ready(function() {

    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#stateform").on("submit", function() {
        console.log("Hello")
        state_changer = document.querySelector("#hidden-state-field")
        if (state_changer.value == 1) {
            state_changer.value = 0;
        } else if (state_changer.value == 0) {
            state_changer.value = 1;
        }
        newMessage($(this));
        return false;
    });
    //console.log("Getting players")
    //var players = JSON.parse(json);
    //console.log("Got players", players)

    $("#hidden-state-field").select();
    updater.poll();
});

function add_player(player_id, player_name, player_state){
    var p = new Player(player_id, player_name, player_state);
    console.log(p.name)
    players.push(p);
    console.log(players);
}


function newMessage(form) {
    var message = form.formToDict();
    console.log("message", message)
    var disabled = form.find("input[type=submit]");
    disabled.disable();
    var address = window.location.pathname+"/change";
    $.postJSON(address, message, function(response) {
        updater.showMessage(response);
        if (message.id) {
            form.parent().remove();
        } else {
            form.find("input[type=text]").val("").select();
            disabled.enable();
        }
    });
}

/*function sendState(form) {
    console.log("send State")
    var state = form.formToDict();
    console.log("State:",state);
    var disabled = form.find("input[type=submit]");
    disabled.disable();
    var address = window.location.pathname+"/state";
    $.postJSON(address, state, function(response) {
        lobbyUpdater.showMessage(response);
        if (state.id) {
            form.parent().remove();
        } else {
            form.find("input[type=text]").val("").select();
            disabled.enable();
        }
    });
}*/

function changeValue() {
    // Changes the value of the button
    button = document.querySelector("#ready-button")
    if (button.value == 1) {
        button.value = 0;
        button.innerHTML = "Ready";
        button.class = "lobby-ready-button not-ready";
    } else if (button.value == 0) {
        button.value = 1;
        button.innerHTML = "Wait"
        button.class = "lobby-ready-button ready";
    }
    // Changes the text on the button
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

jQuery.postJSON = function(url, args, callback) {
    args._xsrf = getCookie("_xsrf");
    $.ajax({url: url,
            data: $.param(args), 
            dataType: "text", 
            type: "POST",
            success: function(response) {
        if (callback) callback(eval("(" + response + ")"));
    }, error: function(response) {
        console.log("ERROR:", response);
    }});
};

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    console.log("Fields:",fields)
    var json = {};
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

jQuery.fn.disable = function() {
    this.enable(false);
    return this;
};

jQuery.fn.enable = function(opt_enable) {
    if (arguments.length && !opt_enable) {
        this.attr("disabled", "disabled");
    } else {
        this.removeAttr("disabled");
    }
    return this;
};

var updater = {

    errorSleepTime: 500,
    cursor: null,
    address: window.location.pathname+"/update",
    poll: function() {
        var args = {"_xsrf": getCookie("_xsrf")};
        if (updater.cursor) args.cursor = updater.cursor;
        $.ajax({url: updater.address, 
                type: "POST", 
                dataType: "text",
                data: $.param(args), 
                success: updater.onSuccess,
                error: updater.onError});
    },

    onSuccess: function(response) {
        try {
            console.log("wooooorks",response)
            //var json = '{"result":true,"count":1}',
            var players = JSON.parse(response);
            console.log(players)
            updater.newPlayer(players);
            //updater.newMessages(eval("(" + response + ")"));
        } catch (e) {
            updater.onError();
            return;
        }
        updater.errorSleepTime = 500;
        window.setTimeout(updater.poll, 0);
    },

    onError: function(response) {
        updater.errorSleepTime *= 2;
        console.log("Poll error; sleeping for", response,updater.errorSleepTime, "ms");
        window.setTimeout(updater.poll, updater.errorSleepTime);
    },

    newPlayer: function(response) {
        console.log("Received",response)
        if (!response.players) return;
        updater.cursor = response.players;
        

        console.log("Going to add player", response.players);
        //for (player in response.players){
            for(var i = 0; i < players.length; i++) {
                if (players[i].id == response.players.id) {

                    players[i].changeState(response.players.state);
                    console.log("updating");
                    updater.updatePlayerEntry(players[i]);
                    break;
                } else {
                    console.log("no ideaaaa",response.players)
                    var p = new Player(response.players.id,
                                       response.players.name,
                                       response.players.state);
                    players.push(p);
                    console.log("new player",p);
                    updater.showPlayerEntry(p);
                }
            }
        //}

        console.log("Updated playeres",players)

    },

    showPlayerEntry: function(player) {
        console.log("Test")
        var existing = $("#p" + player.id);
        if (existing.length > 0) return;
        console.log("geht nocht")
        var node = updater.createLobbyEntry("lobby-table",player.id,
                                    player.name, 
                                    player.state);
        /*console.log(node);
        node.hide();
        $("#lobby-table").append(node);
        node.slideDown();
        console.log("say what?!");*/
    },

    updatePlayerEntry:function(player) {
        var existing = $("#p" + player.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        node.hide();
        $("#inbox").append(node);
        node.slideDown();
    },

    createLobbyEntry:function(parent,id, name, state){
        console.log("creating Lobby Entry");
        var lobby_entry = document.createElement("div");
        console.log("wirklih");
        lobby_entry.className = "lobby-entry";
        console.log(0);
        lobby_entry.id = "p"+toString(id);
        console.log("asdsdfsdgdfgddf");

        var player_state = document.createElement("div");
        player_state.className = "lobby-ready-state";
        var state_icon = document.createElement("i");
        console.log("1")
        if (state == 0) {
            state_icon.className = "fa fa-square"
            state_icon.setAttribute("aria-hidden", "true");
        } else if (state == 1) {
            state_icon.className = "fa fa-check-square"
            state_icon.setAttribute("aria-hidden", "true");
        }
        console.log("2")
        player_state.append(state_icon);

        console.log("3")
        var player_name = document.createElement("p");
        player_name.className = "lobby-name";
        player_name.innerHTML = name;

        clear_div = document.createElement("div");
        clear_div.className = "clear";

        lobby_entry.append(player_state);
        lobby_entry.append(player_name);
        lobby_entry.append(clear_div);
        console.log("created Lobby Entry")
        $("#"+parent).append(lobby_entry);
    },

    newMessages: function(response) {
        console.log("Received",response)
        if (!response.id) return;
        console.log("yep")
        updater.cursor = response.player.id;
        console.log("upd.cursor", updater.cursor)
        

        //updater.cursor = newMessagesssages[messages.length - 1].id;
        //console.log(messages.length, "new messages, cursor:", updater.cursor);
        //for (var i = 0; i < messages.length; i++) {
        //    updater.showMessage(messages[i]);
        //}
    },

    showMessage: function(message) {
        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);
        node.hide();
        $("#inbox").append(node);
        node.slideDown();
    }
};

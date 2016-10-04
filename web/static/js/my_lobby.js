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
var players = "";

function set_players(val)
{
    players = val;
    test = "{ 'players' :"+val +"}";
    console.log("Players: ",players, test);

    check = JSON.parse(test);
    console.log("") 
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
            var player = JSON.parse(response);
            updater.newMessages(player);
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

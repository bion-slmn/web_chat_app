console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);

console.log('Room Name' + roomName)

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");

// adds a new option to 'onlineUsersSelector'
function onlineUsersSelectorAdd(value) {
    if (document.querySelector("option[value='" + value + "']")) return;
    let newOption = document.createElement("option");
    newOption.value = value;
    newOption.innerHTML = value;
    onlineUsersSelector.appendChild(newOption);
}

// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption !== null) oldOption.remove();
}

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function() {
    if (chatMessageInput.value.length === 0) {
      return;
    }
    chatSocket.send(JSON.stringify({
        "message": chatMessageInput.value,
    }));
    // TODO: forward the message to the WebSocket
    chatMessageInput.value = "";
};

let chatSocket = null;

function connect() {
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/");

    chatSocket.onopen = function(e) {
        alert('Connection successful');
    }

    chatSocket.onclose = function(e) {
        alert('Connection lost, retrying in 2 seconds.........');
        setTimeout(function(){
            connect();
        }, 2000)
    }

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data)
        console.log(data)
        
        switch (data.type) {
            case 'chat_message':
                chatLog.value += data.message + '\n';
                break;
            default:
                console.error("Unknown message types");
                break;
        }

        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onerror = function(err) {
        console.log("Websocket enountered and error" + err.message)
        chatSocket.close()
    }
}

connect();
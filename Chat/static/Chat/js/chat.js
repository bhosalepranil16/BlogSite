console.log('in chat.js');

const messageFormInput = document.querySelector('#chat-message-input');
const messageFormButton = document.querySelector('#chat-message-submit');
const messageArea = document.querySelector('.chat-messages');

const roomName = JSON.parse(document.getElementById('room-name').textContent);
const senderUsername = JSON.parse(document.getElementById('sender-username').textContent);
const senderId = JSON.parse(document.getElementById('sender-id').textContent);
const receiverUsername = JSON.parse(document.getElementById('receiver-username').textContent);
const receiverId = JSON.parse(document.getElementById('receiver-id').textContent);

const websocket_url = 'ws://' + window.location.host + '/ws/chat/' + roomName + '/';

const chatSocket = new WebSocket(websocket_url);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    let template;
    if(senderUsername == data.by) {

        template = `
        <div class="chat-message-right pb-4">
            <div>
                <img src="https://bootdey.com/img/Content/avatar/avatar1.png" class="rounded-circle mr-1" alt="Chris Wood" width="40" height="40">
                <div class="text-muted small text-nowrap mt-2">${moment(data.created_at).format('h:mm a')}</div>
            </div>
            <div class="flex-shrink-1 bg-light rounded py-2 px-3 mr-3">
                <div class="mb-1 text-secondary">${data.by}</div>
                ${data.message}
            </div>
        </div>`;
    } else {
        template = `
    <div class="chat-message-left pb-4">
        <div>
            <img src="https://bootdey.com/img/Content/avatar/avatar3.png" class="rounded-circle mr-1" alt="Sharon Lessman" width="40" height="40">
            <div class="text-muted small text-nowrap mt-2">${moment(data.created_at).format('h:mm a')}</div>
        </div>
        <div class="flex-shrink-1 bg-light rounded py-2 px-3 ml-3">
            <div class="mb-1 text-secondary">${data.by}</div>
                ${data.message}
            </div>
        </div>`;
    }

    messageArea.insertAdjacentHTML('beforeend', template);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

messageFormInput.focus();
messageFormInput.onkeyup = function(e) {
    if (e.keyCode === 13) {
        messageFormButton.click();
    }
};

messageFormButton.onclick = function(e) {
    const messageInputDom = messageFormInput;
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'roomName': roomName,
        'message': message,
        'senderId': senderId,
        'receiverId': receiverId,
        'senderUsername': senderUsername
    }));
    messageInputDom.value = '';
};
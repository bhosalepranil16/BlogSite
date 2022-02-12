console.log('in chat.js');

const autoScroll = ()=>{
    //New Message Element
    const newMessage = messageArea.lastElementChild;

    console.log(newMessage);

    //height of the new message
    const newMessageStyles = getComputedStyle(newMessage);
    const newMessageMargin = parseInt(newMessageStyles.marginBottom);
    const newMessageHeight = newMessage.offsetHeight + newMessageMargin;

    //visible height
    const visibleHeight = messageArea.offsetHeight

    //height of messages container
    const containerHeight = messageArea.scrollHeight;

    //how far I have scrolled ?
    const scrollOffset = messageArea.scrollTop + visibleHeight;

    if(containerHeight - newMessageHeight <= scrollOffset) {
        messageArea.scrollTop = messageArea.scrollHeight;
    }
}

autoScroll();

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
                <img src="/static/Chat/images/avatar1.png" class="rounded-circle mr-1" alt=${senderUsername} width="40" height="40">
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
            <img src="/static/Chat/images/avatar2.png" class="rounded-circle mr-1" alt=${senderUsername} width="40" height="40">
            <div class="text-muted small text-nowrap mt-2">${moment(data.created_at).format('h:mm a')}</div>
        </div>
        <div class="flex-shrink-1 bg-light rounded py-2 px-3 ml-3">
            <div class="mb-1 text-secondary">${data.by}</div>
                ${data.message}
            </div>
        </div>`;
    }

    messageArea.insertAdjacentHTML('beforeend', template);
    autoScroll();
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
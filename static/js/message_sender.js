const i2pHost = location.hostname;
const i2pPort = location.port;

const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('messageInput');

let messageQueue = [];
let isRendering = false;

if (messageInput) {
  messageInput.focus();
}

function scrollToTop() {
    messagesDiv.scrollTop = 0;
}

const socket = io.connect(`http://${i2pHost}:${i2pPort}`, {
    transports: ['websocket', 'polling'],
    reconnection: true,
    reconnectionAttempts: 5,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionTimeout: 5000,
    jsonp: false
});

document.getElementById('messageInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (!messageInput.value) return;
        textarea.style.height = '35px';
        sendMessage();
    }
});

socket.on('connect', () => {
    console.log("Connected to chat. use cc('message') to send message");
});


function processQueue() {
    if (messageQueue.length === 0 || isRendering) return;
    isRendering = true;

    const fragment = document.createDocumentFragment();

    messageQueue.forEach(msg => {
        const div = document.createElement('div');
        div.setAttribute('id', 'msg');
        div.innerHTML = msg.replace(/\n/g, '<br>');
        fragment.appendChild(div);
    });

    messagesDiv.append(fragment);

    const isScrolledUp = messagesDiv.scrollTop + messagesDiv.clientHeight < messagesDiv.scrollHeight - 50;
    if (!isScrolledUp) {
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    messageQueue = [];
    isRendering = false;
}

socket.on('message', (data) => {
    messageQueue.push(String(data));

    setTimeout(processQueue, 100);
});

function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value;
    console.log(
    '%c' + message,
    'color: inherit; /* ' + Math.random() + ' */'
    ); // чат теперь не только в ui но и в консоли!
    socket.emit('message', {'message': message});
    input.value = '';
}

function cc(message){  // console chat
    console.log(message);
    socket.emit('message', {'message': message});

    return 'Message sent';
}

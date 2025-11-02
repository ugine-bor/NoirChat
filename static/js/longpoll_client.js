// messageDiv уже определен в chat.html
const messageInput = document.getElementById('messageInput');

if (messageInput) {
    messageInput.focus();
}

let last_ts = 0;
let pollBackoff = 1000; // ms on error
let messageQueue = [];
let isRendering = false;

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

async function pollOnce() {
    try {
        const res = await fetch('/poll?since=' + encodeURIComponent(last_ts), {
            method: 'GET',
            credentials: 'same-origin',
            cache: 'no-cache'
        });
        if (res.status === 403) {
            console.error('Unauthorized (403) when polling');
            return await new Promise(r => setTimeout(r, 5000));
        }
        const data = await res.json();
        if (Array.isArray(data) && data.length) {
            data.forEach(item => {
                try {
                    messageQueue.push(String(decodeHtml(item.message)));
                } catch (e) {
                    // fallback
                    messageQueue.push(String(item.message));
                }
                last_ts = Math.max(last_ts, item.timestamp || last_ts);
            });
            setTimeout(processQueue, 100);
        }
        // reset backoff on success
        pollBackoff = 1000;
    } catch (e) {
        console.error('Long-poll error:', e);
        // backoff before next attempt
        await new Promise(r => setTimeout(r, pollBackoff));
        pollBackoff = Math.min(30000, pollBackoff * 2);
    }
}

async function pollLoop() {
    while (true) {
        await pollOnce();
    }
}

// Start polling when script loads
pollLoop();

function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value;
    console.log(
        '%c' + message,
        'color: inherit; /* ' + Math.random() + ' */'
    ); // чат теперь не только в ui но и в консоли!

    const formData = new FormData();
    formData.append('message', message);

    fetch('/send', {
        method: 'POST',
        body: formData,
        credentials: 'same-origin'
    }).then(response => {
        if (response.ok) {
            input.value = '';
            input.style.height = '35px';  // Возвращаем дефолтную высоту
        } else {
            console.error('Send failed', response.status);
        }
    }).catch(err => {
        console.error('Send error', err);
    });
}

// Console chat function
function cc(message) {  // console chat
    console.log(message);
    const formData = new FormData();
    formData.append('message', message);
    
    fetch('/send', {
        method: 'POST',
        body: formData,
        credentials: 'same-origin'
    });

    return 'Message sent';
}

// Sending messages
if (messageInput) {
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!messageInput.value) return;
            messageInput.style.height = '35px';
            sendMessage();
        }
    });
}

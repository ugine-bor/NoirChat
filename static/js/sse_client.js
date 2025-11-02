const eventSource = new EventSource('/stream');
const messagesDiv = document.getElementById('messages');

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.message) {
        console.log(
            '%c' + decodeHtml(data.message),
            'color: inherit; /* ' + Math.random() + ' */'
        );
        add_message(decodeHtml(data.message));
    }
};

eventSource.onerror = function(event) {
    if (event.readyState === EventSource.CLOSED) {
        console.log('Connection was closed. Retrying...');
        // EventSource автоматически попытается переподключиться
    }
};

// Обработка отправки сообщений
const messageInput = document.getElementById('messageInput');

messageInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        const message = this.value.trim();
        
        if (message) {
            const formData = new FormData();
            formData.append('message', message);
            
            fetch('/send', {
                method: 'POST',
                body: formData,
                credentials: 'same-origin'
            }).then(response => {
                if (response.ok) {
                    this.value = '';
                    updateInputHeight();
                }
            }).catch(error => {
                console.error('Error sending message:', error);
            });
        }
    }
});
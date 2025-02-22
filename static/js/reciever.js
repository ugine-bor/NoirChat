function msgs() {
    return {{ messages | tojson }}
}

function add_message(msg) {

    const div = document.createElement('div');
    div.setAttribute('id', 'msg');
    div.innerHTML = String(msg).replace(/\n/g, '<br>');
    messagesDiv.prepend(div)
}

function deploy_from_database() {

    msgs().forEach(add_message);
}

deploy_from_database()

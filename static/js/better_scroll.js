  function isTextAreaMultiLine(textarea) {
    return textarea.value.includes('\n') || textarea.scrollHeight > textarea.clientHeight;
  }

  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
      const messagesDiv = document.getElementById('messages');
      const messageInput = document.getElementById('messageInput');

      if (messagesDiv.scrollHeight <= messagesDiv.clientHeight) return;

      const activeElement = document.activeElement;
      const isTextAreaActive = (activeElement === messageInput);
      const multiLine = isTextAreaMultiLine(messageInput);

      if (isTextAreaActive && multiLine) {
        return;
      }

      e.preventDefault();

      const scrollStep = 43;

      if (e.key === 'ArrowUp') {
        messagesDiv.scrollTop = Math.round(Math.max(
              -(messagesDiv.scrollHeight - messagesDiv.clientHeight),
              messagesDiv.scrollTop - scrollStep
          ));
      } else if (e.key === 'ArrowDown') {
        messagesDiv.scrollTop = Math.round(Math.min(
            0,
            messagesDiv.scrollTop + scrollStep
        ));
      }
    }
    if (event.ctrlKey) {
      messagesDiv.focus();
    }
  });

  document.addEventListener('keyup', function(event) {
    if (!event.ctrlKey) {
      const textInput = document.getElementById('messageInput');
      textInput.focus();
    }
  });


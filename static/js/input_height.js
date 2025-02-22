function autoResizeTextarea(textarea) {
  textarea.style.height = '35px';
  textarea.style.height = textarea.scrollHeight + 'px';
}

const textarea = document.getElementById('messageInput');

textarea.addEventListener('input', () => {
  autoResizeTextarea(textarea);
});

window.addEventListener('resize', () => {
  autoResizeTextarea(textarea);
});

autoResizeTextarea(textarea);

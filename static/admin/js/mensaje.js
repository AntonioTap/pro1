chatForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;

    if (message.trim() !== '') {
        const newMessage = {
            user: 'admin/cajero',
            content: message
        };
        socket.send(JSON.stringify(newMessage));
        displayMessage(newMessage);
        messageInput.value = '';
    }
});

function displayMessage(message) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.textContent = `${message.user}: ${message.content}`;
    chatMessages.appendChild(messageDiv);

    // Enfocar el área de chat en la parte inferior
    chatMessages.scrollTop = chatMessages.scrollHeight;
};
$(document).ready(function(){
    /* Mostrar u ocultar área de notificaciones/chat */
    $('.btn-Notification').on('click', function(){
        var ContainerNoty = $('.container-notifications');
        var NotificationArea = $('.NotificationArea');
        if(NotificationArea.hasClass('NotificationArea-show') && ContainerNoty.hasClass('container-notifications-show')){
            NotificationArea.removeClass('NotificationArea-show');
            ContainerNoty.removeClass('container-notifications-show');
        } else {
            NotificationArea.addClass('NotificationArea-show');
            ContainerNoty.addClass('container-notifications-show');
        }
    });

    /* Mostrar u ocultar menu principal */
    $('.btn-menu').on('click', function(){
        var navLateral = $('.navLateral');
        var pageContent = $('.pageContent');
        var navOption = $('.navBar-options');
        if(navLateral.hasClass('navLateral-change') && pageContent.hasClass('pageContent-change')){
            navLateral.removeClass('navLateral-change');
            pageContent.removeClass('pageContent-change');
            navOption.removeClass('navBar-options-change');
        } else {
            navLateral.addClass('navLateral-change');
            pageContent.addClass('pageContent-change');
            navOption.addClass('navBar-options-change');
        }
    });

    /* Salir del sistema */
    $('.btn-exit').on('click', function(){
        swal({
            title: 'Desea Salir de Admin',
            text: "Esta apunto de salir de Admin",
            type: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Si, Salir',
            closeOnConfirm: false
        },
        function(isConfirm) {
            if (isConfirm) {
                window.location='/login'; 
            }
        });
    });

    /* Mostrar y ocultar submenus */
    $('.btn-subMenu').on('click', function(){
        var subMenu = $(this).next('ul');
        var icon = $(this).children("span");
        if(subMenu.hasClass('sub-menu-options-show')){
            subMenu.removeClass('sub-menu-options-show');
            icon.addClass('zmdi-chevron-left').removeClass('zmdi-chevron-down');
        } else {
            subMenu.addClass('sub-menu-options-show');
            icon.addClass('zmdi-chevron-down').removeClass('zmdi-chevron-left');
        }
    });

    /* Inicializar WebSocket */
    const socket = new WebSocket('ws://tu-servidor-web/chat'); // Cambia la URL a tu endpoint de WebSockets

    socket.addEventListener('open', () => {
        console.log('Conexión WebSocket establecida.');
    });

    socket.addEventListener('message', (event) => {
        const message = JSON.parse(event.data);
        displayMessage(message);
    });

    const chatForm = document.getElementById('chat-form');
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
    }

    // Inicializar Scrollbars
    $(".NotificationArea, .pageContent").mCustomScrollbar({
        theme: "dark-thin",
        scrollbarPosition: "inside",
        autoHideScrollbar: true,
        scrollButtons: { enable: true }
    });

    $(".navLateral-body").mCustomScrollbar({
        theme: "light-thin",
        scrollbarPosition: "inside",
        autoHideScrollbar: true,
        scrollButtons: { enable: true }
    });
});

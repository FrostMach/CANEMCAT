$(document).ready(function () {
    // Detectar si estamos en la landing page (raíz del dominio)
    const isLandingPage = window.location.pathname === '/';

    if (isLandingPage) {
        // Si estamos en la landing, permitir que la animación se ejecute siempre
        localStorage.removeItem('chatAnimationPlayed'); // Borra cualquier estado previo para reiniciar la animación
    }

    // Comprobar si la animación ya se ejecutó
    if (localStorage.getItem('chatAnimationPlayed') === 'true') {
        // Añadir clase para desactivar animaciones
        $('body').addClass('no-animation');
    } else {
        // Marcar que la animación ya se ejecutó
        localStorage.setItem('chatAnimationPlayed', 'true');
    }

    // Resto del código para el chatbot
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    $('#chat-icon').click(function () {
        $('#chatModal').modal('show');
    });

    $('#sendMessageButton').click(function () {
        var message = $('#user_input').val();
        if (message.trim() === '') return;

        $('#chatbox').append('<div><b>Usuario:</b> ' + message + '</div>');
        $('#user_input').val('');

        $.ajax({
            url: '/chat/',
            method: 'POST',
            data: {
                'message': message,
                'csrfmiddlewaretoken': csrfToken,
            },
            success: function (data) {
                $('#chatbox').append('<div><b>ChatBot:</b> ' + data.response + '</div>');
                $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
            },
            error: function () {
                $('#chatbox').append('<div><b>Error:</b> No se pudo obtener respuesta del chatbot.</div>');
            },
        });
    });

    $('#user_input').on('keypress', function (e) {
        if (e.which === 13) {
            $('#sendMessageButton').click();
        }
    });
});



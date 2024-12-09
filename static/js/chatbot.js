$(document).ready(function() {
    // Obtener el token CSRF desde el campo oculto dentro del modal
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    
    // Abre el modal al hacer clic en el icono de chat
    $('#chat-icon').click(function() {
        $('#chatModal').modal('show');
    });

    // Función para enviar el mensaje del usuario
    $('#sendMessageButton').click(function() {
        var message = $('#user_input').val();
        if (message.trim() === '') return; // No enviar si está vacío

        // Mostrar el mensaje del usuario en el chatbox
        $('#chatbox').append('<div><b>Usuario:</b> ' + message + '</div>');
        
        // Limpiar el campo de entrada
        $('#user_input').val('');

        // Enviar el mensaje al servidor usando jQuery AJAX
        $.ajax({
            url: '/chat/',  // La URL a la que se hace la solicitud
            method: 'POST',
            data: {
                'message': message,  // El mensaje que el usuario escribió
                'csrfmiddlewaretoken': csrfToken  // Usar el token CSRF desde el campo oculto
            },
            success: function(data) {
                // Mostrar la respuesta del chatbot en el chatbox
                $('#chatbox').append('<div><b>ChatBot:</b> ' + data.response + '</div>');
                
                // Desplazar el chatbox hacia abajo para mostrar el mensaje más reciente
                $('#chatbox').scrollTop($('#chatbox')[0].scrollHeight);
            },
            error: function() {
                // Si ocurre un error, mostrar un mensaje en el chatbox
                $('#chatbox').append('<div><b>Error:</b> No se pudo obtener respuesta del chatbot.</div>');
            }
        });
    });

    // También asociar la función al presionar "Enter"
    $('#user_input').on('keypress', function(e) {
        if (e.which === 13) {  // 13 es la tecla Enter
            $('#sendMessageButton').click();
        }
    });
});

$(document).ready(function () {
    // Obtener el CSRF token desde el formulario oculto
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    var calendar = $('#calendar').fullCalendar({
        locale: 'es',
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },

        events: '/get_events/',  // Ruta para obtener los eventos desde Django
        selectable: true,
        selectHelper: true,
        editable: true,
        eventLimit: true,
        eventResizableFromStart: true,

        select: function (start, end, allDay) {
            var title = prompt("Ingrese el título del evento");
            if (title) {
                var start_time = $.fullCalendar.formatDate(start, "YYYY-MM-DD HH:mm:ss");
                var end_time = $.fullCalendar.formatDate(end, "YYYY-MM-DD HH:mm:ss");
                console.log('Fecha de inicio:', start_time);
                console.log('Fecha de fin:', end_time);

                $.ajax({
                    type: "POST",  // Usamos POST para enviar datos de manera segura
                    url: '/add_event/',  // Ruta para agregar el evento
                    data: {
                        'title': title,
                        'start': start_time,
                        'end': end_time,
                        'csrfmiddlewaretoken': csrf_token  // CSRF Token
                    },
                    dataType: "json",
                    success: function (data) {
                        calendar.fullCalendar('refetchEvents');  // Recargar eventos después de añadir
                        // alert("Evento agregado correctamente");
                    },
                    error: function () {
                        alert('¡Hubo un problema al agregar el evento!');
                    }
                });
            }
        },

        eventResize: function (event, delta, revertFunc) {
            // Formatear las fechas de inicio y fin para enviarlas al servidor
            var start_time = $.fullCalendar.formatDate(event.start, "YYYY-MM-DD HH:mm:ss");
            var end_time = $.fullCalendar.formatDate(event.end, "YYYY-MM-DD HH:mm:ss");
            var title = event.title;
            var id = event.id;

            // Realizar una solicitud AJAX para actualizar el evento
            $.ajax({
                type: "POST",
                url: '/update/', // Ruta para actualizar el evento
                data: {
                    'id': id,
                    'title': title,
                    'start': start_time,
                    'end': end_time,
                    'csrfmiddlewaretoken': csrf_token // CSRF Token
                },
                dataType: "json",
                success: function (response) {
                    if (response.success) {
                        // alert('Evento actualizado correctamente.');
                    } else {
                        alert('Error al actualizar el evento: ' + response.message);
                        revertFunc(); // Revertir los cambios si el servidor indica un error
                    }
                },
                error: function () {
                    alert('Hubo un problema al intentar actualizar el evento.');
                    revertFunc(); // Revertir los cambios si ocurre un error en la solicitud
                }
            });
        },


        eventDrop: function (event) {
            var start_time = $.fullCalendar.formatDate(event.start, "YYYY-MM-DD HH:mm:ss");
            var end_time = $.fullCalendar.formatDate(event.end, "YYYY-MM-DD HH:mm:ss");
            var title = event.title;
            var id = event.id;

            $.ajax({
                type: "POST",  // Usamos POST para actualizar el evento
                url: '/update/',  // Ruta para actualizar el evento
                data: {
                    'title': title,
                    'start': start_time,
                    'end': end_time,
                    'id': id,
                    'csrfmiddlewaretoken': csrf_token  // CSRF Token
                },
                dataType: "json",
                success: function () {
                    calendar.fullCalendar('refetchEvents');  // Recargar eventos después de mover
                    // alert('Evento actualizado correctamente');
                },
                error: function () {
                    alert('¡Hubo un problema al actualizar el evento!');
                }
            });
        },

        eventClick: function (event) {
            if (confirm("¿Estás seguro de que deseas eliminar este evento?")) {
                var id = event.id;  // Asegúrate de que esto sea el id correcto
                $.ajax({
                    type: "POST",  // Cambié a POST para evitar posibles problemas con la manipulación de datos
                    url: '/remove/',  // Ruta para eliminar el evento
                    data: {
                        'id': id,
                        'csrfmiddlewaretoken': csrf_token  // CSRF Token
                    },
                    dataType: "json",
                    success: function () {
                        calendar.fullCalendar('refetchEvents');  // Recargar eventos después de eliminar
                        // alert('Evento eliminado correctamente');
                    },
                    error: function () {
                        alert('¡Hubo un problema al eliminar el evento!');
                    }
                });
            }
        }

    });
    
    // Rellenar el selector de años dinámicamente
    var currentYear = new Date().getFullYear();
    for (var i = currentYear - 5; i <= currentYear + 5; i++) {
        $('#year-select').append($('<option>', {
            value: i,
            text: i
        }));
    }
    $('#year-select').val(currentYear); // Seleccionar el año actual por defecto

    // Manejar el cambio de mes/año
    $('#month-select, #year-select').change(function () {
        var selectedMonth = $('#month-select').val(); // Obtener el mes seleccionado
        var selectedYear = $('#year-select').val();   // Obtener el año seleccionado

        // Cambiar la vista del calendario al mes y año seleccionados
        var newDate = moment([selectedYear, selectedMonth]); // Crear una fecha con Moment.js
        calendar.fullCalendar('gotoDate', newDate); // Navegar a la fecha
    });
});

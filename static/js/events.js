document.addEventListener("DOMContentLoaded", () => {
    const eventsList = document.getElementById("events-list");
    
    // Simulamos los eventos del usuario (En una app real, estos se obtendrían desde una API)
    const userEvents = [
        { id: 1, description: "Reunión de trabajo", date: "2024-12-05", start_time: "09:00", end_time: "10:00", color: "#ff5733" },
        { id: 2, description: "Cita médica", date: "2024-12-07", start_time: "11:30", end_time: "12:30", color: "#33c1ff" },
        { id: 3, description: "Cena de amigos", date: "2024-12-10", start_time: "19:00", end_time: "22:00", color: "#9bff33" },
    ];

    // Función para cargar los eventos en la lista
    function loadUserEvents() {
        eventsList.innerHTML = ""; // Limpiar la lista antes de cargar nuevos eventos
        userEvents.forEach(event => {
            const listItem = document.createElement("li");
            listItem.classList.add("event-item");
            listItem.innerHTML = `
                <strong>${event.description}</strong><br>
                Fecha: ${event.date} - Hora: ${event.start_time} - Color: <span style="background-color:${event.color};">${event.color}</span>
            `;
            eventsList.appendChild(listItem);
        });
    }

    // Llamamos a la función para cargar los eventos cuando la página se carga
    loadUserEvents();

    // Función para obtener los eventos por fecha
    function getEventsByDate(date) {
        return userEvents.filter(event => event.date === date);
    }

    // Agregar la lógica para mostrar eventos en el calendario
    function displayEventsInCalendar(events, calendarBody) {
        const rows = calendarBody.getElementsByTagName('tr');
        Array.from(rows).forEach(row => {
            const cells = row.getElementsByTagName('td');
            Array.from(cells).forEach(cell => {
                const dayNumber = cell.querySelector('.day-number');
                if (dayNumber) {
                    const day = parseInt(dayNumber.innerText);
                    const cellDate = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                    const dayEvents = getEventsByDate(cellDate);
                    dayEvents.forEach(event => {
                        const eventElement = document.createElement("div");
                        eventElement.classList.add("event");
                        eventElement.style.backgroundColor = event.color;
                        eventElement.innerText = event.description;
                        cell.appendChild(eventElement);
                    });
                }
            });
        });
    }

    // Actualiza los eventos en el calendario
    function updateCalendar() {
        // Lógica para actualizar el calendario
        const calendarBody = document.getElementById("calendar-body");
        // Llamar a la función de display para mostrar los eventos
        displayEventsInCalendar(userEvents, calendarBody);
    }

    // Llamar a updateCalendar() cuando se navegue entre los meses
    document.getElementById("prev-month").addEventListener("click", () => {
        // Lógica para ir al mes anterior
        updateCalendar();
    });

    document.getElementById("next-month").addEventListener("click", () => {
        // Lógica para ir al siguiente mes
        updateCalendar();
    });
});


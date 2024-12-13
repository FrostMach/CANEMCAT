document.addEventListener("DOMContentLoaded", () => {
    const prevButton = document.getElementById("prev-month");
    const nextButton = document.getElementById("next-month");
    const calendarBody = document.getElementById("calendar-body");
    const monthYearLabel = document.getElementById("month-year");

    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();
    let events = {};

    // Lógica para actualizar el calendario
    function updateCalendar() {
        const monthNames = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
        monthYearLabel.innerText = `${monthNames[currentMonth]} ${currentYear}`;

        const firstDay = new Date(currentYear, currentMonth, 1).getDay();
        const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

        calendarBody.innerHTML = "";

        let row = document.createElement("tr");
        for (let i = 0; i < firstDay; i++) {
            row.appendChild(document.createElement("td"));
        }

        for (let day = 1; day <= daysInMonth; day++) {
            if ((firstDay + day - 1) % 7 === 0 && day !== 1) {
                calendarBody.appendChild(row);
                row = document.createElement("tr");
            }

            const cell = document.createElement("td");
            const date = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

            const dayNumber = document.createElement("span");
            dayNumber.innerText = day;
            dayNumber.classList.add("day-number");
            cell.appendChild(dayNumber);

            if (events[date]) {
                events[date].forEach(event => {
                    const eventElement = document.createElement("div");
                    eventElement.classList.add("event");
                    eventElement.style.backgroundColor = event.color;
                    eventElement.innerText = event.description;

                    // Añadir un evento de clic a cada evento dentro de la celda
                    eventElement.addEventListener("click", () => {
                        window.openEditModal(event); // Llamar al modal de edición
                    });

                    cell.appendChild(eventElement);
                });
            }

            cell.addEventListener("click", () => {
                window.openNewEventModal(date); // Llama a la función para abrir el modal
            });            

            row.appendChild(cell);
        }
        calendarBody.appendChild(row);
    }


    // Cargar eventos
    function loadEvents() {
        fetch(`/events/${currentYear}/${currentMonth + 1}/`)
            .then(response => response.json())
            .then(data => {
                events = {};
                data.events.forEach(event => {
                    if (!events[event.date]) {
                        events[event.date] = [];
                    }

                    events[event.date].push(event);
                });
                updateCalendar();
            })
            .catch(error => {
                console.error("Error al cargar eventos:", error);
            });
    }

    prevButton.addEventListener("click", () => {
        if (currentMonth === 0) {
            currentMonth = 11;
            currentYear--;
        } else {
            currentMonth--;
        }
        loadEvents();
    });

    nextButton.addEventListener("click", () => {
        if (currentMonth === 11) {
            currentMonth = 0;
            currentYear++;
        } else {
            currentMonth++;
        }
        loadEvents();
    });

    loadEvents();
});


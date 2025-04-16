// Calendar functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize FullCalendar
    const calendarEl = document.getElementById('calendar');
    
    if (calendarEl) {
        // Parse events from the data attribute
        const eventsData = calendarEl.dataset.events;
        const events = eventsData ? JSON.parse(eventsData) : [];
        
        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: window.innerWidth < 768 ? 'listWeek' : 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,listWeek'
            },
            themeSystem: 'bootstrap5',
            events: events,
            eventTimeFormat: {
                hour: '2-digit',
                minute: '2-digit',
                meridiem: 'short'
            },
            eventClick: function(info) {
                showEventDetails(info.event);
            },
            dayMaxEvents: true,
            height: 'auto',
            windowResize: function(view) {
                if (window.innerWidth < 768) {
                    calendar.changeView('listWeek');
                } else {
                    calendar.changeView('dayGridMonth');
                }
            }
        });
        
        calendar.render();
        
        // Show event details in a modal
        function showEventDetails(event) {
            const modalTitle = document.querySelector('#eventModal .modal-title');
            const modalBody = document.querySelector('#eventModal .modal-body');
            const modalFooter = document.querySelector('#eventModal .modal-footer');
            
            if (modalTitle && modalBody) {
                modalTitle.textContent = event.title;
                
                let content = `
                    <p><strong>Date:</strong> ${event.start ? event.start.toLocaleDateString() : 'N/A'}</p>
                    <p><strong>Time:</strong> ${event.start ? event.start.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : 'All day'}</p>
                `;
                
                if (event.extendedProps && event.extendedProps.description) {
                    content += `<p>${event.extendedProps.description.replace(/\n/g, '<br>')}</p>`;
                }
                
                modalBody.innerHTML = content;
                
                // Check if this is an appointment (not a medication)
                if (!event.id.startsWith('med_')) {
                    // Add delete button for appointments
                    modalFooter.innerHTML = `
                        <form action="/calendar/delete/${event.id}" method="post">
                            <button type="submit" class="btn btn-danger" data-confirm="Are you sure you want to delete this appointment?">Delete</button>
                        </form>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    `;
                } else {
                    modalFooter.innerHTML = `
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    `;
                }
                
                const eventModal = new bootstrap.Modal(document.getElementById('eventModal'));
                eventModal.show();
            }
        }
        
        // Handle form submission for adding new appointments
        const appointmentForm = document.getElementById('appointmentForm');
        if (appointmentForm) {
            appointmentForm.addEventListener('submit', function(e) {
                // Form validation is handled by the server-side
            });
        }
    }
});

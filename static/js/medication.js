// Medication tracking functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize medication time picker
    const timeOfDayInput = document.getElementById('time_of_day');
    if (timeOfDayInput) {
        // Add time suggestions
        const suggestions = [
            { text: 'Morning (8:00 AM)', value: '08:00' },
            { text: 'Noon (12:00 PM)', value: '12:00' },
            { text: 'Evening (6:00 PM)', value: '18:00' },
            { text: 'Night (10:00 PM)', value: '22:00' }
        ];
        
        const suggestionContainer = document.createElement('div');
        suggestionContainer.className = 'mt-2 d-flex flex-wrap gap-2';
        
        suggestions.forEach(suggestion => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-sm btn-outline-secondary';
            btn.textContent = suggestion.text;
            btn.addEventListener('click', function() {
                if (timeOfDayInput.value) {
                    // Add to existing times if not already included
                    const times = timeOfDayInput.value.split(', ');
                    if (!times.includes(suggestion.value)) {
                        times.push(suggestion.value);
                        timeOfDayInput.value = times.join(', ');
                    }
                } else {
                    timeOfDayInput.value = suggestion.value;
                }
            });
            suggestionContainer.appendChild(btn);
        });
        
        // Add custom time input
        const customTimeContainer = document.createElement('div');
        customTimeContainer.className = 'mt-2 input-group';
        
        const customTimeInput = document.createElement('input');
        customTimeInput.type = 'time';
        customTimeInput.className = 'form-control';
        customTimeInput.id = 'custom_time';
        
        const addButton = document.createElement('button');
        addButton.type = 'button';
        addButton.className = 'btn btn-secondary';
        addButton.textContent = 'Add Time';
        addButton.addEventListener('click', function() {
            const customTime = document.getElementById('custom_time').value;
            if (customTime) {
                if (timeOfDayInput.value) {
                    const times = timeOfDayInput.value.split(', ');
                    if (!times.includes(customTime)) {
                        times.push(customTime);
                        timeOfDayInput.value = times.join(', ');
                    }
                } else {
                    timeOfDayInput.value = customTime;
                }
            }
        });
        
        customTimeContainer.appendChild(customTimeInput);
        customTimeContainer.appendChild(addButton);
        
        // Add helpers after the input
        timeOfDayInput.parentNode.insertBefore(suggestionContainer, timeOfDayInput.nextSibling);
        timeOfDayInput.parentNode.insertBefore(customTimeContainer, suggestionContainer.nextSibling);
        
        // Add helper text
        const helpText = document.createElement('small');
        helpText.className = 'form-text text-muted';
        helpText.textContent = 'Enter times in 24-hour format (HH:MM) separated by commas';
        timeOfDayInput.parentNode.insertBefore(helpText, customTimeContainer.nextSibling);
    }
    
    // Set up end date logic based on frequency
    const frequencySelect = document.getElementById('frequency');
    const endDateInput = document.getElementById('end_date');
    
    if (frequencySelect && endDateInput) {
        frequencySelect.addEventListener('change', function() {
            // If "as_needed" is selected, end date is optional
            if (this.value === 'as_needed') {
                endDateInput.required = false;
                const label = document.querySelector('label[for="end_date"]');
                if (label) {
                    label.textContent = 'End Date (Optional)';
                }
            } else {
                // End date is still optional but recommended for other frequencies
                const label = document.querySelector('label[for="end_date"]');
                if (label) {
                    label.textContent = 'End Date (Recommended)';
                }
            }
        });
    }
    
    // Setup medication reminders table interactions
    const medicationTable = document.getElementById('medicationsTable');
    if (medicationTable) {
        // Add click handler for medication details
        medicationTable.querySelectorAll('.medication-row').forEach(row => {
            row.addEventListener('click', function() {
                // Toggle visibility of details row
                const detailsRow = this.nextElementSibling;
                if (detailsRow && detailsRow.classList.contains('medication-details')) {
                    detailsRow.classList.toggle('d-none');
                    
                    // Toggle arrow icon
                    const arrow = this.querySelector('.details-toggle i');
                    if (arrow) {
                        arrow.classList.toggle('fa-chevron-down');
                        arrow.classList.toggle('fa-chevron-up');
                    }
                }
            });
        });
        
        // Prevent detail toggle when clicking delete button
        medicationTable.querySelectorAll('.delete-medication').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                if (!confirm('Are you sure you want to delete this medication?')) {
                    e.preventDefault();
                }
            });
        });
    }
});

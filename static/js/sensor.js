/**
 * ESP32 Sensor Data Manager
 * Handles:
 * - Visualizing sensor data with Chart.js
 * - Managing sensor data UI
 * - Handling ESP32 API integration
 */

document.addEventListener('DOMContentLoaded', function() {
    // Unit change based on sensor type
    const sensorTypeSelect = document.querySelector('#sensor_type');
    const unitSelect = document.querySelector('#unit');
    
    if (sensorTypeSelect && unitSelect) {
        sensorTypeSelect.addEventListener('change', function() {
            updateUnitOptions(this.value);
        });
        
        // Run once on page load to set initial options
        if (sensorTypeSelect.value) {
            updateUnitOptions(sensorTypeSelect.value);
        }
    }
    
    // Handle delete buttons
    document.querySelectorAll('.delete-reading').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            if (confirm('Are you sure you want to delete this reading?')) {
                const readingId = this.getAttribute('data-id');
                
                fetch(`/api/sensor_data/${readingId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Remove the row from the table or reload the page
                        const row = this.closest('tr');
                        if (row) {
                            row.remove();
                        } else {
                            window.location.reload();
                        }
                    } else {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting the reading');
                });
            }
        });
    });
    
    /**
     * Update unit selection options based on sensor type
     */
    function updateUnitOptions(sensorType) {
        // Clear current options
        unitSelect.innerHTML = '';
        
        // Set appropriate units based on sensor type
        if (sensorType === 'temperature') {
            addOption(unitSelect, 'celsius', '°C');
            addOption(unitSelect, 'fahrenheit', '°F');
        } else if (sensorType === 'heart_rate') {
            addOption(unitSelect, 'bpm', 'bpm');
        } else if (sensorType === 'blood_pressure') {
            addOption(unitSelect, 'mmHg', 'mmHg');
        } else if (sensorType === 'blood_oxygen') {
            addOption(unitSelect, 'percent', '%');
        } else if (sensorType === 'glucose') {
            addOption(unitSelect, 'mg/dL', 'mg/dL');
            addOption(unitSelect, 'mmol/L', 'mmol/L');
        } else if (sensorType === 'ecg') {
            addOption(unitSelect, 'mv', 'mV');
        } else {
            // Default options
            addOption(unitSelect, 'celsius', '°C');
            addOption(unitSelect, 'fahrenheit', '°F');
            addOption(unitSelect, 'bpm', 'bpm');
            addOption(unitSelect, 'mmHg', 'mmHg');
            addOption(unitSelect, 'percent', '%');
            addOption(unitSelect, 'mg/dL', 'mg/dL');
            addOption(unitSelect, 'other', 'Other');
        }
    }
    
    /**
     * Helper to add an option to a select element
     */
    function addOption(select, value, text) {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = text;
        select.appendChild(option);
    }
    
    /**
     * ESP32 Mock Device Simulation
     * For development and testing purposes
     */
    const mockDeviceButton = document.getElementById('simulate-esp32');
    if (mockDeviceButton) {
        mockDeviceButton.addEventListener('click', function() {
            // Generate random sensor data
            const sensorTypes = ['temperature', 'heart_rate', 'blood_pressure', 'blood_oxygen', 'glucose'];
            const randomType = sensorTypes[Math.floor(Math.random() * sensorTypes.length)];
            
            let value, unit;
            
            // Generate realistic values based on sensor type
            switch (randomType) {
                case 'temperature':
                    value = (Math.random() * 2 + 36).toFixed(1); // 36-38°C
                    unit = 'celsius';
                    break;
                case 'heart_rate':
                    value = Math.floor(Math.random() * 40 + 60); // 60-100 bpm
                    unit = 'bpm';
                    break;
                case 'blood_pressure':
                    value = Math.floor(Math.random() * 40 + 110); // 110-150 mmHg (systolic)
                    unit = 'mmHg';
                    break;
                case 'blood_oxygen':
                    value = (Math.random() * 5 + 94).toFixed(1); // 94-99%
                    unit = 'percent';
                    break;
                case 'glucose':
                    value = Math.floor(Math.random() * 50 + 80); // 80-130 mg/dL
                    unit = 'mg/dL';
                    break;
            }
            
            // Prepare the mock data payload
            const mockData = {
                sensor_type: randomType,
                value: parseFloat(value),
                unit: unit,
                device_id: 'esp32-simulator',
                notes: 'Simulated reading'
            };
            
            // Send to the API using the new WebSocket-enabled endpoint
            fetch('/api/sensor_data/esp32', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(mockData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show a temporary success message
                    const container = document.querySelector('.col-lg-8.mb-4 .card-body');
                    if (container) {
                        const alert = document.createElement('div');
                        alert.className = 'alert alert-success alert-dismissible fade show';
                        alert.innerHTML = `
                            <strong>Success!</strong> Simulated ${randomType} reading sent: ${value} ${unit}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        `;
                        container.prepend(alert);
                        
                        // Auto-dismiss after 5 seconds
                        setTimeout(() => {
                            alert.classList.remove('show');
                            setTimeout(() => alert.remove(), 150);
                        }, 5000);
                    }
                    
                    // No need to reload - WebSockets will update the UI automatically
                } else {
                    alert('Error: ' + (data.error || 'Unknown error'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while sending simulated data');
            });
        });
    }
});
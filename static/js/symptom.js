// Symptom checker functionality

document.addEventListener('DOMContentLoaded', function() {
    // Handle symptom form submission
    const symptomForm = document.getElementById('symptomForm');
    const symptomInput = document.getElementById('symptoms');
    const resultsContainer = document.getElementById('symptomResults');
    
    if (symptomForm && symptomInput) {
        // Add common symptom suggestions
        const commonSymptoms = [
            'Headache', 'Fever', 'Cough', 'Sore throat', 'Stomach pain',
            'Nausea', 'Fatigue', 'Dizziness', 'Rash', 'Joint pain',
            'Back pain', 'Shortness of breath'
        ];
        
        const suggestionContainer = document.createElement('div');
        suggestionContainer.className = 'mt-2 mb-3';
        suggestionContainer.innerHTML = '<p class="mb-2 small text-muted">Common symptoms:</p>';
        
        const suggestionButtonContainer = document.createElement('div');
        suggestionButtonContainer.className = 'd-flex flex-wrap gap-2';
        
        commonSymptoms.forEach(symptom => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'btn btn-sm btn-outline-secondary';
            btn.textContent = symptom;
            btn.addEventListener('click', function() {
                if (symptomInput.value) {
                    // Check if the symptom is already mentioned
                    if (!symptomInput.value.toLowerCase().includes(symptom.toLowerCase())) {
                        symptomInput.value += ', ' + symptom.toLowerCase();
                    }
                } else {
                    symptomInput.value = symptom.toLowerCase();
                }
            });
            suggestionButtonContainer.appendChild(btn);
        });
        
        suggestionContainer.appendChild(suggestionButtonContainer);
        symptomInput.parentNode.insertBefore(suggestionContainer, symptomInput.nextSibling);
        
        // Clear button
        const clearButton = document.createElement('button');
        clearButton.type = 'button';
        clearButton.className = 'btn btn-sm btn-outline-danger mt-2';
        clearButton.textContent = 'Clear symptoms';
        clearButton.addEventListener('click', function() {
            symptomInput.value = '';
        });
        
        suggestionContainer.appendChild(clearButton);
    }
    
    // Add copy to clipboard functionality for recommendations
    if (resultsContainer) {
        const copyButtons = resultsContainer.querySelectorAll('.copy-recommendations');
        copyButtons.forEach(button => {
            button.addEventListener('click', function() {
                const listId = this.dataset.target;
                const list = document.getElementById(listId);
                
                if (list) {
                    // Get all list items
                    const items = list.querySelectorAll('li');
                    let text = '';
                    
                    // Build text from list items
                    items.forEach(item => {
                        text += '- ' + item.textContent + '\n';
                    });
                    
                    // Copy to clipboard
                    navigator.clipboard.writeText(text).then(() => {
                        // Show success message
                        const originalText = this.textContent;
                        this.textContent = 'Copied!';
                        this.classList.remove('btn-outline-primary');
                        this.classList.add('btn-success');
                        
                        // Revert button after 2 seconds
                        setTimeout(() => {
                            this.textContent = originalText;
                            this.classList.remove('btn-success');
                            this.classList.add('btn-outline-primary');
                        }, 2000);
                    })
                    .catch(err => {
                        console.error('Error copying text: ', err);
                        alert('Failed to copy to clipboard');
                    });
                }
            });
        });
        
        // Add print function for recommendations
        const printButtons = resultsContainer.querySelectorAll('.print-recommendations');
        printButtons.forEach(button => {
            button.addEventListener('click', function() {
                window.print();
            });
        });
    }
});

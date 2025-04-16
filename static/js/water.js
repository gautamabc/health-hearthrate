// Water tracking functionality

document.addEventListener('DOMContentLoaded', function() {
    // Update water progress bar
    function updateWaterProgress() {
        const progressBar = document.getElementById('waterProgressBar');
        const totalWater = document.getElementById('totalWater');
        const targetWater = document.getElementById('targetWater');
        
        if (progressBar && totalWater && targetWater) {
            const current = parseInt(totalWater.textContent);
            const target = parseInt(targetWater.textContent);
            
            const percentage = Math.min(Math.round((current / target) * 100), 100);
            
            progressBar.style.width = percentage + '%';
            progressBar.setAttribute('aria-valuenow', percentage);
            
            // Update color based on progress
            if (percentage < 30) {
                progressBar.classList.remove('bg-success', 'bg-warning');
                progressBar.classList.add('bg-danger');
            } else if (percentage < 70) {
                progressBar.classList.remove('bg-success', 'bg-danger');
                progressBar.classList.add('bg-warning');
            } else {
                progressBar.classList.remove('bg-warning', 'bg-danger');
                progressBar.classList.add('bg-success');
            }
        }
    }
    
    // Initialize progress bar
    updateWaterProgress();
    
    // Quick add water buttons
    const quickAddButtons = document.querySelectorAll('.quick-add-water');
    const waterAmountInput = document.getElementById('amount');
    
    if (quickAddButtons.length && waterAmountInput) {
        quickAddButtons.forEach(button => {
            button.addEventListener('click', function() {
                const amount = parseInt(this.dataset.amount);
                waterAmountInput.value = amount;
            });
        });
    }
    
    // Handle water intake form submission
    const waterForm = document.getElementById('waterIntakeForm');
    if (waterForm) {
        waterForm.addEventListener('submit', function(e) {
            // Could implement AJAX submission here
            // For now, we'll let the form submit normally
        });
    }
    
    // Setup water intake history interaction
    const deleteWaterButtons = document.querySelectorAll('.delete-water-intake');
    if (deleteWaterButtons.length) {
        deleteWaterButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to delete this water intake entry?')) {
                    e.preventDefault();
                }
            });
        });
    }
    
    // Create wave animation effect in water tracker card
    const waterCard = document.querySelector('.water-tracker-card');
    if (waterCard) {
        const waveContainer = document.createElement('div');
        waveContainer.className = 'position-absolute bottom-0 start-0 w-100 overflow-hidden';
        waveContainer.style.height = '15px';
        waveContainer.style.opacity = '0.7';
        waveContainer.style.zIndex = '0';
        
        const wave = document.createElement('div');
        wave.className = 'w-100';
        wave.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" class="w-100" style="margin-bottom: -7px;">
                <path fill="rgba(var(--bs-info-rgb), 0.5)" fill-opacity="1" d="M0,192L48,160C96,128,192,64,288,69.3C384,75,480,149,576,165.3C672,181,768,139,864,144C960,149,1056,203,1152,202.7C1248,203,1344,149,1392,122.7L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
            </svg>
        `;
        
        waveContainer.appendChild(wave);
        waterCard.appendChild(waveContainer);
        waterCard.style.position = 'relative';
        
        // Animate the wave
        let position = 0;
        setInterval(() => {
            position -= 1;
            if (position <= -1440) {
                position = 0;
            }
            wave.style.transform = `translateX(${position}px)`;
        }, 50);
    }
});

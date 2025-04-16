// Diet tracking functionality

document.addEventListener('DOMContentLoaded', function() {
    // Setup date picker for diet entries
    const dietDateInput = document.getElementById('date');
    if (dietDateInput) {
        // When date changes, redirect to show that date's entries
        dietDateInput.addEventListener('change', function() {
            // Could implement AJAX here to fetch entries for the selected date
            // For simplicity, we'll just reload the page with the new date
            // This would be implemented in a more sophisticated way in a real app
        });
    }
    
    // Initialize nutrition chart if element exists
    const nutritionChartCanvas = document.getElementById('nutritionChart');
    if (nutritionChartCanvas) {
        const totalCalories = parseFloat(nutritionChartCanvas.dataset.calories || 0);
        const totalProtein = parseFloat(nutritionChartCanvas.dataset.protein || 0);
        const totalCarbs = parseFloat(nutritionChartCanvas.dataset.carbs || 0);
        const totalFat = parseFloat(nutritionChartCanvas.dataset.fat || 0);
        
        // Calculate macronutrient percentages
        const proteinCalories = totalProtein * 4; // 4 calories per gram of protein
        const carbCalories = totalCarbs * 4;      // 4 calories per gram of carbs
        const fatCalories = totalFat * 9;         // 9 calories per gram of fat
        
        // Calculate percentages
        const total = proteinCalories + carbCalories + fatCalories;
        
        let proteinPercentage = 0;
        let carbPercentage = 0;
        let fatPercentage = 0;
        
        if (total > 0) {
            proteinPercentage = Math.round((proteinCalories / total) * 100);
            carbPercentage = Math.round((carbCalories / total) * 100);
            fatPercentage = Math.round((fatCalories / total) * 100);
        }
        
        // Create chart
        const nutritionChart = new Chart(nutritionChartCanvas, {
            type: 'doughnut',
            data: {
                labels: ['Protein', 'Carbs', 'Fat'],
                datasets: [{
                    data: [proteinPercentage, carbPercentage, fatPercentage],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(255, 99, 132, 0.8)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                return `${label}: ${value}%`;
                            }
                        }
                    }
                }
            }
        });
        
        // Add calorie counter in the center
        const chartContainer = nutritionChartCanvas.parentElement;
        const calorieCounter = document.createElement('div');
        calorieCounter.className = 'position-absolute top-50 start-50 translate-middle text-center';
        calorieCounter.innerHTML = `
            <div class="h3 mb-0">${totalCalories}</div>
            <div class="small">calories</div>
        `;
        chartContainer.style.position = 'relative';
        chartContainer.appendChild(calorieCounter);
    }
    
    // Setup food suggestions
    const foodItemsTextarea = document.getElementById('food_items');
    const mealTypeSelect = document.getElementById('meal_type');
    
    if (foodItemsTextarea && mealTypeSelect) {
        // Common food suggestions by meal type
        const foodSuggestions = {
            breakfast: [
                'Oatmeal with berries',
                'Eggs and whole grain toast',
                'Greek yogurt with honey and nuts',
                'Smoothie with spinach, banana, and almond milk',
                'Whole grain cereal with milk'
            ],
            lunch: [
                'Grilled chicken salad',
                'Turkey sandwich on whole grain bread',
                'Quinoa bowl with vegetables',
                'Lentil soup with a side salad',
                'Tuna wrap with mixed greens'
            ],
            dinner: [
                'Baked salmon with roasted vegetables',
                'Stir-fried tofu with brown rice',
                'Lean beef stew with vegetables',
                'Whole grain pasta with tomato sauce',
                'Grilled vegetables with quinoa'
            ],
            snack: [
                'Apple slices with peanut butter',
                'Carrot sticks with hummus',
                'Greek yogurt with berries',
                'Handful of mixed nuts',
                'Whole grain crackers with cheese'
            ]
        };
        
        // Add suggestion button after the textarea
        const suggestionContainer = document.createElement('div');
        suggestionContainer.className = 'mt-2 mb-3';
        suggestionContainer.innerHTML = '<p class="mb-2 small text-muted">Common suggestions:</p>';
        
        const suggestionButtonContainer = document.createElement('div');
        suggestionButtonContainer.className = 'd-flex flex-wrap gap-2';
        suggestionContainer.appendChild(suggestionButtonContainer);
        
        // Update suggestions when meal type changes
        function updateSuggestions() {
            const mealType = mealTypeSelect.value;
            suggestionButtonContainer.innerHTML = '';
            
            if (foodSuggestions[mealType]) {
                foodSuggestions[mealType].forEach(suggestion => {
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.className = 'btn btn-sm btn-outline-secondary';
                    btn.textContent = suggestion;
                    btn.addEventListener('click', function() {
                        if (foodItemsTextarea.value) {
                            foodItemsTextarea.value += '\n' + suggestion;
                        } else {
                            foodItemsTextarea.value = suggestion;
                        }
                    });
                    suggestionButtonContainer.appendChild(btn);
                });
            }
        }
        
        mealTypeSelect.addEventListener('change', updateSuggestions);
        
        // Insert suggestions after textarea
        foodItemsTextarea.parentNode.insertBefore(suggestionContainer, foodItemsTextarea.nextSibling);
        
        // Initialize with current meal type
        updateSuggestions();
    }
});

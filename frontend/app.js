document.addEventListener('DOMContentLoaded', function() {
    const citySelect = document.getElementById('citySelect');
    const weatherInfo = document.getElementById('weatherInfo');
    const getWeatherBtn = document.getElementById('getWeather');
    const chatInput = document.getElementById('chatInput');
    const sendMessageBtn = document.getElementById('sendMessage');
    const chatMessages = document.getElementById('chatMessages');
    const chatToggle = document.getElementById('chatToggle');
    const chatClose = document.getElementById('chatClose');
    const chatPopup = document.getElementById('chatPopup');
    const API_BASE_URL = 'http://localhost:8000';

    let isLoading = false;

    chatToggle.addEventListener('click', () => {
        chatPopup.classList.add('active');
        chatInput.focus();
    });

    chatClose.addEventListener('click', () => {
        chatPopup.classList.remove('active');
    });

    document.addEventListener('click', (e) => {
        if (!chatPopup.contains(e.target) && !chatToggle.contains(e.target)) {
            chatPopup.classList.remove('active');
        }
    });

    console.log('Fetching cities from:', `${API_BASE_URL}/`);
    fetch(`${API_BASE_URL}/`)
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Cities data:', data);
            if (!data.available_cities || !Array.isArray(data.available_cities)) {
                throw new Error('Invalid data format received from server');
            }
            data.available_cities.forEach(city => {
                const option = document.createElement('option');
                option.value = city;
                option.textContent = city;
                citySelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching cities:', error);
            showError(`Failed to load cities: ${error.message}. Please check if the backend service is running.`);
        });

    getWeatherBtn.addEventListener('click', fetchWeatherData);

    function fetchWeatherData() {
        const selectedCity = citySelect.value;
        if (!selectedCity) {
            showError('Please select a city first');
            return;
        }

        if (isLoading) return;
        
        isLoading = true;
        setLoadingState(true);

        console.log('Fetching weather data for:', selectedCity);
        fetch(`${API_BASE_URL}/predictions/${selectedCity}`)
            .then(response => {
                console.log('Weather data response status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Weather data received:', data);
                updateWeatherDisplay(data);
                weatherInfo.classList.add('visible');
            })
            .catch(error => {
                console.error('Error fetching weather data:', error);
                showError(`Failed to fetch weather data: ${error.message}`);
            })
            .finally(() => {
                isLoading = false;
                setLoadingState(false);
            });
    }

    function updateWeatherDisplay(data) {
        document.getElementById('currentTemp').textContent = data.current_temperature.toFixed(1);
        document.getElementById('currentHumidity').textContent = data.current_humidity.toFixed(1);
        document.getElementById('lastUpdated').textContent = data.last_updated;

        document.getElementById('predictionDate').textContent = data.prediction_date;
        document.getElementById('predictedTemp').textContent = data.predicted_temperature.toFixed(1);

        const historicalContainer = document.getElementById('historicalData');
        historicalContainer.innerHTML = ''; // Clear existing data

        data.historical_data.forEach(entry => {
            const historyEntry = document.createElement('div');
            historyEntry.className = 'historical-entry';
            
            historyEntry.innerHTML = `
                <div class="date">
                    <i class="far fa-calendar-alt"></i>
                    ${entry.date}
                </div>
                <div class="readings">
                    <span>
                        <i class="fas fa-temperature-high"></i>
                        ${entry.temperature.toFixed(1)}°C
                    </span>
                    <span>
                        <i class="fas fa-tint"></i>
                        ${entry.humidity.toFixed(1)}%
                    </span>
                </div>
            `;
            
            historicalContainer.appendChild(historyEntry);
        });

        weatherInfo.classList.add('visible');
    }

    function setLoadingState(loading) {
        getWeatherBtn.disabled = loading;
        getWeatherBtn.innerHTML = loading ? 
            '<i class="fas fa-spinner fa-spin"></i> Loading...' : 
            '<i class="fas fa-search"></i> Get Weather';
    }

    function showError(message) {
        console.error('Error:', message);
        alert(message);
    }

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'assistant'}`;
        messageDiv.innerHTML = `
            <div class="message-content">
                ${message}
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        chatInput.value = '';

        addMessage(message, true);

        try {
            chatInput.disabled = true;
            sendMessageBtn.disabled = true;

            // Send message to API
            const response = await fetch(`${API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) {
                throw new Error('Failed to get response from assistant');
            }

            const data = await response.json();
            addMessage(data.response);
        } catch (error) {
            console.error('Chat error:', error);
            addMessage('Sorry, I encountered an error. Please try again.');
        } finally {
            chatInput.disabled = false;
            sendMessageBtn.disabled = false;
            chatInput.focus();
        }
    }

    sendMessageBtn.addEventListener('click', sendMessage);

    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}); 
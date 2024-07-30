document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('searchBtn');
    const zipInput = document.getElementById('zip_code');
    const toggleTempBtn = document.getElementById('toggleTemp');
    const logoutBtn = document.getElementById('logoutBtn');  // Reference to the logout button

    function handleSearch() {
        WeatherData();
    }

    function toggleTemperature() {
        const tempSpan = document.getElementById('temp');
        let currentTemp = tempSpan.innerText;
        if (currentTemp.includes('°C')) {
            let celsiusTemp = parseFloat(currentTemp);
            let fahrenheitTemp = celsiusToFahrenheit(celsiusTemp);
            tempSpan.innerText = `${fahrenheitTemp.toFixed(2)}°F`;
        } else {
            let fahrenheitTemp = parseFloat(currentTemp.split('°')[0]);
            let celsiusTemp = fahrenheitToCelsius(fahrenheitTemp);
            tempSpan.innerText = `${celsiusTemp.toFixed(2)}°C`;
        }
    }

    function celsiusToFahrenheit(celsius) {
        return (celsius * 9/5) + 32;
    }

    function fahrenheitToCelsius(fahrenheit) {
        return (fahrenheit - 32) * 5/9;
    }

    // Logout functionality
    logoutBtn.addEventListener('click', function() {
        window.location.href = '/logout'; 
    });

    searchBtn.addEventListener('click', handleSearch);
    zipInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            handleSearch();
        }
    });
    toggleTempBtn.addEventListener('click', toggleTemperature);
});

async function WeatherData() {
    const zipCode = document.getElementById('zip_code').value;
    try {
        const response = await fetch(`/search_zip?zip_code=${zipCode}`);
        const data = await response.json();

        if (data.error) {
            alert("Please enter a valid zip code.");
            resetWeatherData();
            return;
        }

        updateWeatherData(data);
    } catch (error) {
        alert("Unable to fetch weather data. Please check your internet connection.");
        resetWeatherData();
    }
}

function updateWeatherData(data) {
    document.getElementById('city-name').innerText = data.city;
    document.getElementById('temp').innerText = `${kelvinToCelsius(data.weather.list[0].main.temp)}°C`;
    document.getElementById('description').innerText = data.weather.list[0].weather[0].description;
    document.getElementById('humidity').innerText = `${data.weather.list[0].main.humidity}% Humidity`;
    document.getElementById('wind-speed').innerText = `${data.weather.list[0].wind.speed} km/h Wind Speed`;
    document.getElementById('icon').src = determineWeatherIcon(data.weather.list[0].weather[0].main.toLowerCase());
}

function kelvinToCelsius(kelvin) {
    return (kelvin - 273.15).toFixed(2);
}

function determineWeatherIcon(weatherMain) {
    switch (weatherMain) {
        case 'clear': return 'static/images/clear.png';
        case 'clouds': return 'static/images/clouds.png';
        case 'rain': return 'static/images/rain.png';
        case 'snow': return 'static/images/snow.png';
        case 'thunderstorm': return 'static/images/thunderstorm.png';
        case 'drizzle': return 'static/images/drizzle.png';
        default: return 'static/images/clear.png';
    }
}

function resetWeatherData() {
    const defaultText = '--';
    document.getElementById('city-name').innerText = defaultText;
    document.getElementById('temp').innerText = `${defaultText}°C`;
    document.getElementById('description').innerText = 'City Name';
    document.getElementById('humidity').innerText = `${defaultText}% Humidity`;
    document.getElementById('wind-speed').innerText = `${defaultText} km/h Wind Speed`;
    document.getElementById('icon').src = 'images/weather icon.png';
}

//storing initial (default) values to variables in local storage
window.addEventListener("load", (event) => {
    if (!localStorage.getItem("vehicle_type")) localStorage.setItem("vehicle_type", "car");
    if (!localStorage.getItem("weather_type")) localStorage.setItem("weather_type", "normal");
    if (!localStorage.getItem("safety_value")) localStorage.setItem("safety_value", "0.5");
    if (!localStorage.getItem("distance_value")) localStorage.setItem("distance_value", "0.5");
    if (!localStorage.getItem("speed_value")) localStorage.setItem("speed_value", "0.5");
    if (!localStorage.getItem("dayofweek")) localStorage.setItem("dayofweek", "sunday");
    if (!localStorage.getItem("time_value")) localStorage.setItem("time_value", "13:30");
    if (!localStorage.getItem("paths_value")) localStorage.setItem("paths_value", "1");
});

//gets initial html elements for each query
const setvehicle_dropdown = document.getElementById('vehicle-type');

const safety_slider = document.getElementById("safety-slider");
const safety_coef = document.getElementById("safety-value");

const distance_slider = document.getElementById("distance-slider");
const distance_coef = document.getElementById("distance-value");

const speed_slider = document.getElementById("speed-slider");
const speed_coef = document.getElementById("speed-value");

const reset_values_button = document.getElementById("reset-values-button");

const setdayofweek_dropdown = document.getElementById('day-of-week');
const time_select = document.getElementById('time-set');

const setweather_dropdown = document.getElementById('weather-type');

const setnumpaths_input = document.getElementById('paths-input');

//for each query, load value for respective variable set in localStorage 
setvehicle_dropdown.value = localStorage.getItem("vehicle_type");
//for each query, listen for changes and set that change to new value
setvehicle_dropdown.addEventListener('change', function(event) {
    localStorage.setItem("vehicle_type", event.target.value);
});

safety_slider.value = localStorage.getItem("safety_value");
safety_coef.innerHTML = (safety_slider.value * 100).toFixed(0) + "%";
safety_slider.oninput = function() {
    safety_coef.innerHTML = (this.value * 100).toFixed(0) + "%";
    localStorage.setItem("safety_value", safety_slider.value);
}

distance_slider.value = localStorage.getItem("distance_value");
distance_coef.innerHTML = (distance_slider.value * 100).toFixed(0) + "%";
distance_slider.oninput = function() {
    distance_coef.innerHTML = (this.value * 100).toFixed(0) + "%";
    localStorage.setItem("distance_value", distance_slider.value);
}

speed_slider.value = localStorage.getItem("speed_value");
speed_coef.innerHTML = (speed_slider.value * 100).toFixed(0) + "%";
speed_slider.oninput = function() {
    speed_coef.innerHTML = (this.value * 100).toFixed(0) + "%";
    localStorage.setItem("speed_value", speed_slider.value);
}

reset_values_button.addEventListener('click', function () {
    safety_slider.value = 0.5;
    safety_coef.innerHTML = 50 + "%";
    localStorage.setItem("safety_value", safety_slider.value);
    distance_slider.value = 0.5;
    distance_coef.innerHTML = 50 + "%";
    localStorage.setItem("distance_value", distance_slider.value);
    speed_slider.value = 0.5;
    speed_coef.innerHTML = 50 + "%";
    localStorage.setItem("speed_value", speed_slider.value);
});

setdayofweek_dropdown.value = localStorage.getItem("dayofweek");
setdayofweek_dropdown.addEventListener('change', function(event) {
    localStorage.setItem("dayofweek", event.target.value);
});

time_select.value = localStorage.getItem("time_value");
time_select.addEventListener('change', function(event) {
    localStorage.setItem("time_value", event.target.value);
});

setweather_dropdown.value = localStorage.getItem("weather_type");
setweather_dropdown.addEventListener('change', function(event) {
    localStorage.setItem("weather_type", event.target.value);
});

setnumpaths_input.value = localStorage.getItem("paths_value");
setnumpaths_input.addEventListener('change', function(event) {
    localStorage.setItem("paths_value", setnumpaths_input.value);
});
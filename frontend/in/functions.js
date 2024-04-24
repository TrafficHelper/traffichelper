//REGULAR

//funciton to reset the values all to 50%
function reset_values() { 
    safety_slider.value = 50;
    safety_value.innerHTML = 50 + "%";
    distance_slider.value = 50;
    distance_value.innerHTML = 50 + "%";
    speed_slider.value = 50;
    speed_value.innerHTML = 50 + "%";
}

function set_vehicle_type(vehicle_type) {
    //set vehicle type
    console.log(vehicle_type);
}

function set_start_end_points(start, end) {
    //set start & end points
    console.log(start);
    console.log(end);
}

function set_route_preferences(safety_val, distance_val, speed_val) {
    //set route preferences
    console.log(safety_val);
    console.log(distance_val);
    console.log(speed_val);
}

function set_time_preferences(day_of_week, time_of_day) {
    //set time preferences
    console.log(day_of_week);
    console.log(time_of_day);
}

function set_weather_type(weather_type) {
    //set weather type
    console.log(weather_type);
}

function set_num_paths(paths) {
    //set number of paths
    console.log(paths);
}

//safety slider variables
const safety_slider = document.getElementById("safety-slider");
const safety_value = document.getElementById("safety-value");
safety_value.innerHTML = safety_slider.value + "%";

//distance slider variables
const distance_slider = document.getElementById("distance-slider");
const distance_value = document.getElementById("distance-value");
distance_value.innerHTML = distance_slider.value + "%";

//speed slider variables
const speed_slider = document.getElementById("speed-slider");
const speed_value = document.getElementById("speed-value");
speed_value.innerHTML = speed_slider.value + "%";

//update function whenever slider is changed
safety_slider.oninput = function() {
    safety_value.innerHTML = this.value + "%";
    console.log("safety %: " + this.value);
}

//update function whenever slider is changed
distance_slider.oninput = function() {
    distance_value.innerHTML = this.value + "%";
    console.log("distance %: " + this.value);
}

//update function whenever slider is changed
speed_slider.oninput = function() {
    speed_value.innerHTML = this.value + "%";
    console.log("speed %: " + this.value);
}

const reset_values_button = document.getElementById("reset-values-button");
reset_values_button.addEventListener('click', function () {
    reset_values();
});

const center = {
    lat: 45.424721,
    lng: -75.695000,
};

//actual values for start and end pos
var start_pos = center;
var end_pos = center;

//temporary (for updating values so then they are accessible outside functions as well)
var currentstart_pos = center;
var currentend_pos = center;

//the starting marker on the map
const start_marker = L.marker(center, {
    draggable: true,
    icon: L.icon({
    iconUrl: './map-icons/start_icon.png',
      iconSize: [30, 50], //[width, height] (px)
      iconAnchor: [15, 50], //point of the icon which will correspond to marker's location
      popupAnchor: [1, -45] //point by which the popup should open relative to the iconAnchor
    })
  }).addTo(map);

  start_marker.on('dragend', function (event) {
    const start_marker = event.target;
    currentstart_pos = start_marker.getLatLng();
});

//the destination marker on the map
const destination_marker = L.marker(center, {
    draggable: true,
    icon: L.icon({
      iconUrl: './map-icons/end_icon.png',
      iconSize: [30, 50],
      iconAnchor: [15, 50],
      popupAnchor: [1, -45] 
    })
  }).addTo(map);

  destination_marker.on('dragend', function (event) {
    const destination_marker = event.target;
    currentend_pos = destination_marker.getLatLng();
});

start_marker.bindPopup('start').openPopup();
destination_marker.bindPopup('end').openPopup();

const setstart_button = document.getElementById('set-start-button');
const setend_button = document.getElementById('set-end-button');

//when the side buttons are clicked it sets the start and end to these values
setstart_button.addEventListener('click', function() {
    start_pos = currentstart_pos;
    console.log("starting coords: " + start_pos);
});
setend_button.addEventListener('click', function() {
    end_pos = currentend_pos;
    console.log("destination coords: " + end_pos);
});


const setvehicle_dropdown = document.getElementById('vehicle-type');
var vehicle_type = setvehicle_dropdown.value;

setvehicle_dropdown.addEventListener('change', function(event) {
    vehicle_type = event.target.value;
    console.log("selected vehicle type: " + vehicle_type);
});

const setdayofweek_dropdown = document.getElementById('day-of-week');
const time_select = document.getElementById('time-set');
var day_of_week = 'setdayofweek_dropdown.value';
var time_value = time_select.value; //this is 24h type --> ex. 02:01 PM reads 14:01

setdayofweek_dropdown.addEventListener('change', function(event) {
    day_of_week = event.target.value;
    console.log("selected day of the week: " + day_of_week);
});

time_select.addEventListener('change', function(event) {
    time_value = event.target.value;
    console.log("selected time value (converted): " + time_value);
});

const setweather_dropdown = document.getElementById('weather-type');
var weather_type = setweather_dropdown.value;

setweather_dropdown.addEventListener('change', function(event) {
    weather_type = event.target.value;
    console.log("selected weather type: " + weather_type);
});

const setnumpaths_input = document.getElementById('paths-input');
var num_paths = setnumpaths_input.value;

setnumpaths_input.addEventListener('change', function(event) {
    num_paths = setnumpaths_input.value;
    console.log("selected number of paths: " + num_paths);
});


//submit button runs all
const submit_button = document.getElementById('submit-form-button');

submit_button.addEventListener('click', function() {
    set_vehicle_type(vehicle_type);
    set_start_end_points(start_pos, end_pos);
    set_route_preferences(safety_slider.value, distance_slider.value, speed_slider.value);
    set_time_preferences(day_of_week, time_value);
    set_weather_type(weather_type);
    set_num_paths(num_paths);
});




//ADMIN Control


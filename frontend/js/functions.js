//REGULAR


function set_vehicle_type() {
    //set vehicle type
    var vehicle_type = localStorage.getItem("vehicle_type");
    console.log(vehicle_type);
}

function set_start_end_points() {
    //set start & end point
    var start_point = localStorage.getItem("start_point");
    var end_point = localStorage.getItem("end_point");
    console.log(start_point);
    console.log(end_point);
}

function set_route_preferences() {
    //set route preferences
    var safety_val = localStorage.getItem("safety_value");
    var distance_val = localStorage.getItem("distance_value");
    var speed_val = localStorage.getItem("speed_value");

    console.log(safety_val);
    console.log(distance_val);
    console.log(speed_val);
}

function set_time_preferences() {
    //set time preferences
    var dayofweek = localStorage.getItem("dayofweek");
    var time_value = localStorage.getItem("time_value");
    console.log(dayofweek);
    console.log(time_value);
}

function set_weather_type() {
    //set weather type
    var weather_type = localStorage.getItem("weather_type");
    console.log(weather_type);
}

function set_num_paths() {
    //set number of paths
    var paths_value = localStorage.getItem("paths_value")
    console.log(paths_value);
}

//function to reset the values all to 50%
function reset_values() { 
    safety_slider.value = 50;
    safety_value.innerHTML = 50 + "%";
    localStorage.setItem("safety_value", safety_slider.value);
    distance_slider.value = 50;
    distance_value.innerHTML = 50 + "%";
    localStorage.setItem("distance_value", distance_slider.value);
    speed_slider.value = 50;
    speed_value.innerHTML = 50 + "%";
    localStorage.setItem("speed_value", speed_slider.value);
}

//vehicle type variables
const setvehicle_dropdown = document.getElementById('vehicle-type');
if(setvehicle_dropdown) {
    setvehicle_dropdown.value = localStorage.getItem("vehicle_type");
    var vehicle_type = setvehicle_dropdown.value;
    localStorage.setItem("vehicle_type", vehicle_type);
    setvehicle_dropdown.addEventListener('change', function(event) {
        vehicle_type = event.target.value;
        localStorage.setItem("vehicle_type", vehicle_type);
    });
}

//safety slider variables
const safety_slider = document.getElementById("safety-slider");
const safety_value = document.getElementById("safety-value");
if(safety_slider) {
    safety_slider.value = localStorage.getItem("safety_value");
    safety_value.innerHTML = safety_slider.value + "%";
    localStorage.setItem("safety_value", safety_slider.value);
    //update function whenever slider is changed
    safety_slider.oninput = function() {
        safety_value.innerHTML = this.value + "%";
        localStorage.setItem("safety_value", safety_slider.value);
    }
}

//distance slider variables
const distance_slider = document.getElementById("distance-slider");
const distance_value = document.getElementById("distance-value");
if(distance_slider) {
    distance_slider.value = localStorage.getItem("distance_value");
    distance_value.innerHTML = distance_slider.value + "%";
    localStorage.setItem("distance_value", distance_slider.value);
    //update function whenever slider is changed
    distance_slider.oninput = function() {
        distance_value.innerHTML = this.value + "%";
        localStorage.setItem("distance_value", distance_slider.value);
    }
}

//speed slider variables
const speed_slider = document.getElementById("speed-slider");
const speed_value = document.getElementById("speed-value");
if(speed_slider) {
    speed_value.value = localStorage.getItem("speed_value");
    speed_value.innerHTML = speed_slider.value + "%";
    localStorage.setItem("speed_value", speed_slider.value);
    //update function whenever slider is changed
    speed_slider.oninput = function() {
        speed_value.innerHTML = this.value + "%";
        localStorage.setItem("speed_value", speed_slider.value);
    }
}

const reset_values_button = document.getElementById("reset-values-button");
if(reset_values_button) {
    reset_values_button.addEventListener('click', function () {
        reset_values();
    });
}

//day of we
const setdayofweek_dropdown = document.getElementById('day-of-week');
const time_select = document.getElementById('time-set');

if(setdayofweek_dropdown) {
    setdayofweek_dropdown.value = localStorage.getItem("dayofweek");
    var day_of_week = setdayofweek_dropdown.value;
    localStorage.setItem("dayofweek", day_of_week);
    setdayofweek_dropdown.addEventListener('change', function(event) {
        day_of_week = event.target.value;
        localStorage.setItem("dayofweek", day_of_week);
    });
}

if(time_select) {
    time_select.value = localStorage.getItem("time_value");
    var time_value = time_select.value; //this is 24h type --> ex. 02:01 PM reads 14:01
    localStorage.setItem("time_value", time_value);
    time_select.addEventListener('change', function(event) {
        time_value = event.target.value;
        localStorage.setItem("time_value", time_value);
    });
}


const setweather_dropdown = document.getElementById('weather-type');

if(setweather_dropdown) {
    setweather_dropdown.value = localStorage.getItem("weather_type");
    var weather_type = setweather_dropdown.value;
    localStorage.setItem("weather_type", weather_type);
    setweather_dropdown.addEventListener('change', function(event) {
        weather_type = event.target.value;
        localStorage.setItem("weather_type", weather_type);
    });
}

const setnumpaths_input = document.getElementById('paths-input');

if(setnumpaths_input) {
    setnumpaths_input.value = localStorage.getItem("paths_value");
    var num_paths = setnumpaths_input.value;
    localStorage.setItem("paths_value", num_paths);
    setnumpaths_input.addEventListener('change', function(event) {
        num_paths = setnumpaths_input.value;
        localStorage.setItem("paths_value", num_paths);
    });
}


const map_cont = document.getElementById('map');

if(map_cont) {
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
        iconUrl: 'frontend/assets/icons/start_icon.png',
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
            iconUrl: 'frontend/assets/icons/end_icon.png',
            iconSize: [30, 50],
            iconAnchor: [15, 50],
            popupAnchor: [1, -45] 
        })
        }).addTo(map);
    
        destination_marker.on('dragend', function (event) {
        const destination_marker = event.target;
        currentend_pos = destination_marker.getLatLng();
    });
}

const setstart_button = document.getElementById('set-start-button');
const setend_button = document.getElementById('set-end-button');
const starting_address = document.getElementById('starting-address');
const ending_address = document.getElementById('ending-address');

if(setstart_button) {
    setstart_button.addEventListener('click', function() {
        if(starting_address.value) {
            //PRIORITIZES address over LOCATION point
            //check if valid address, then convert to coordinates.
            start_pos = starting_address.value //replace starting_address with conversion.
            localStorage.setItem("start_point", start_pos);
            console.log(localStorage.getItem("start_point"));
        }
        else {
            start_pos = currentstart_pos;
            localStorage.setItem("start_point", start_pos);
            console.log(localStorage.getItem("start_point"));
        }
    })
}

if(setend_button) {
    setend_button.addEventListener('click', function() {
        if(ending_address.value) {
            //PRIORITIZES address over LOCATION point
            //check if valid address, then convert to coordinates.
            end_pos = ending_address.value //replace ending_address with conversion.
            localStorage.setItem("end_point", end_pos);
            console.log(localStorage.getItem("end_point"));
        }
        else {
            end_pos = currentend_pos;
            localStorage.setItem("end_point", end_pos);
            console.log(localStorage.getItem("end_point"));
        }
    })
}



//submit button runs all
const submit_button = document.getElementById('submit-form-button');

if(submit_button) {
    submit_button.addEventListener('click', function() {
        set_vehicle_type(vehicle_type);
        set_start_end_points(start_pos, end_pos);
        set_route_preferences(safety_value, distance_value, speed_value);
        set_time_preferences(day_of_week, time_value);
        set_weather_type(weather_type);
        set_num_paths(num_paths);
    });
}
var results_map = L.map('results-map', {
    center: [43.00, -79.00],
    zoom: 15
}).setView([45.424721, -75.695000], 12);

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20
}).addTo(results_map);

function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

var start_coord;
var end_coord;

var results_value_table = document.getElementById('values-table-component');

const prefs_url = 'http://127.0.0.1:8000/prefer';
const api_url = 'http://127.0.0.1:8000/saferoute';

function confirmPreferences() {
    var vehicle_type = localStorage.getItem("vehicle_type").toUpperCase();
    var environment = localStorage.getItem("weather_type").toUpperCase();
    var safety_value = localStorage.getItem("safety_value");
    var distance_value = localStorage.getItem("distance_value");
    var speed_value = localStorage.getItem("speed_value");

    let prefsForm = {
        "vehicletype": vehicle_type,
        "environment": environment,
        "PathChoices": {
          "safety": parseFloat(safety_value),
          "time_of_day": parseFloat(speed_value),
          "distance": parseFloat(distance_value)
        }
    }
    
    console.log(prefsForm);

    fetch(prefs_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(prefsForm)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
}

function Submit_Form() {
    var start_point = localStorage.getItem("start_point");
    var end_point = localStorage.getItem("end_point");
    var day_of_week = localStorage.getItem("dayofweek").toUpperCase;
    var time_of_day = localStorage.getItem("time_value");
    var pathCountInput = localStorage.getItem("paths_value");

    let formData = {
        "StartEnd": {
            "start_address": start_point,
            "destination_address": end_point
        },
        "StartTime": {
            "day_of_week": day_of_week,
            "time_of_day": time_of_day
        },
        "path_count": parseInt(pathCountInput)
    }

    fetch(api_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(dataList => { 
        const unparsed_data = JSON.stringify(dataList);
        const data = JSON.parse(unparsed_data);
        console.log(data)
        
        var numroutes = data.length;

        for(let i=0; i<numroutes; i++) {
            var coordinates = data[i].routes;

            //changing coordinates = ["(x1,y1)", "(x2,y2)" ...] to coordinates = [[x1, y1], [x2, y2] ...]
            coordinates = coordinates.map(coord => {
                coord = coord.slice(1, -1);
                return coord.split(',').map(Number);
            });

            const start_coord = {
                lat: coordinates[0][0],
                lng: coordinates[0][1],
            };
            const end_coord = {
                lat: coordinates[coordinates.length - 1][0],
                lng: coordinates[coordinates.length - 1][1],
            };

            //the starting marker on the map
            L.marker(start_coord, {
                draggable: false,
                icon: L.icon({
                    iconUrl: 'frontend/assets/icons/start_icon.png',
                    iconSize: [36, 60], //[width, height] (px)
                    iconAnchor: [15, 50], //point of the icon which will correspond to marker's location
                    popupAnchor: [1, -45] //point by which the popup should open relative to the iconAnchor
                })
            }).addTo(results_map);

            //the destination marker on the map
            L.marker(end_coord, {
                draggable: false,
                icon: L.icon({
                    iconUrl: 'frontend/assets/icons/end_icon.png',
                    iconSize: [36, 60],
                    iconAnchor: [15, 50],
                    popupAnchor: [1, -45] 
                })
            }).addTo(results_map);

            var risk_val = data[i].risk;
            var traveltime_val = data[i].traveltime;
            var distance_val = data[i].distance;
            var color = getRandomColor()
            
            var route = L.polyline(coordinates, {color: color, weight: 2.75, opacity: 1});
            route.addTo(results_map);
            

            if(results_value_table) {
                var newRow = results_value_table.insertRow();
                var routeNumberCell = newRow.insertCell();
                var riskCell = newRow.insertCell();
                var traveltimeCell = newRow.insertCell();
                var distanceCell = newRow.insertCell();
                var colorCell = newRow.insertCell();
        
                routeNumberCell.textContent = i + 1;
                riskCell.textContent = risk_val.toFixed(0);
                traveltimeCell.textContent = traveltime_val.toFixed(0); 
                distanceCell.textContent = distance_val.toFixed(0);
                
                var colorDiv = document.createElement('div');
                colorDiv.style.width = '20px';
                colorDiv.style.height = '20px'; 
                colorDiv.style.backgroundColor = color;
                colorDiv.style.border = '1px solid black';
        
                colorCell.appendChild(colorDiv);
            }
        }
    })
}

confirmPreferences();
Submit_Form();
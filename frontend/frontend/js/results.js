//sets initial theme
localStorage.setItem("maptheme", "dark");

theme = localStorage.getItem("maptheme");

var road_display = document.getElementById("paths-info-box");

//initializes map (for results with leaflet)
var results_map = L.map('results-map', {
    center: [43.00, -79.00],
    zoom: 15
}).setView([45.424721, -75.695000], 12);

if(theme == "dark"){
    //adds tilelayer to map
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>',
        maxZoom: 20,
    }).addTo(results_map);
} else {
    //adds tilelayer to map
    L.tileLayer('    https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>',
        maxZoom: 20,
    }).addTo(results_map);
}

change_theme_button = document.getElementById("light-dark-button");
moon = document.getElementById("moon");

if(theme == "dark") {
    change_theme_button.style.background = "#ffffff";
    moon.style.boxShadow = "0.35rem 0.35rem 0 0 #191919";
} else {
    change_theme_button.style.background = "#191919";
    moon.style.boxShadow = "0.35rem 0.35rem 0 0 #ffffff";
}

change_theme_button.addEventListener('click', function() {
    theme = localStorage.getItem("maptheme");

    if(theme == "dark") {
        //adds tilelayer to map
        L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>',
            maxZoom: 20,
        }).addTo(results_map);
        //sets initial theme
        localStorage.setItem("maptheme", "light");
        change_theme_button.style.background = "#191919";
        moon.style.boxShadow = "0.35rem 0.35rem 0 0 #ffffff";
    }
    else {
        //adds tilelayer to map
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>',
            maxZoom: 20,
        }).addTo(results_map);

        //sets initial theme
        localStorage.setItem("maptheme", "dark");
        change_theme_button.style.background = "#ffffff";
        moon.style.boxShadow = "0.35rem 0.35rem 0 0 #191919";
    }
});


/**
 * Generates a random color (random hex code)
 * @param none
 * @returns {[string]} [random hex code color]
 */
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) color += letters[Math.floor(Math.random() * 16)];
    return color;
}

//set variables for start and end coords
var start_coord;
var end_coord;

//html element for results value table
var results_value_table = document.getElementById('values-table-component');

//sets prefs and api url for frontend and backend connection
const prefs_url = 'http://127.0.0.1:8000/prefer';
const api_url = 'http://127.0.0.1:8000/saferoute';

/**
 * Submits the user preferences and fetch POST and GETs to api and backend
 * @param none
 * @returns none
 */
function Submit_Prefences() {
    //fetches user input data from localStorage
    var vehicle_type = localStorage.getItem("vehicle_type").toUpperCase();
    var environment = localStorage.getItem("weather_type").toUpperCase();
    var safety_value = localStorage.getItem("safety_value");
    var distance_value = localStorage.getItem("distance_value");
    var speed_value = localStorage.getItem("speed_value");

    //creates a json style form to send to API for the backend to process
    let prefsForm = {
        "vehicletype": vehicle_type,
        "environment": environment,
        "PathChoices": {
          "safety": parseFloat(safety_value),
          "time_of_day": parseFloat(speed_value),
          "distance": parseFloat(distance_value)
        }
    }

    //fetch POST method
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
    //if success, console.log success
    .then(dataList => {
        console.log('Success:', dataList);
    })
    //catches error
    .catch(error => {
        console.error('Error:', error);
    });
}

/**
 * Submit all user inputs (including start and end points)
 * @param none
 * @returns none
 */
function Submit_All() {
    //fetches user inputs 
    var start_point = localStorage.getItem("start_point");
    var end_point = localStorage.getItem("end_point");
    var day_of_week = localStorage.getItem("dayofweek").toUpperCase;
    var time_of_day = localStorage.getItem("time_value");
    var pathCountInput = localStorage.getItem("paths_value");

    //json style form data
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

    //fetch POST method
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
    //if success for backend sending back results
    .then(dataList => { 
        
        const unparsed_data = JSON.stringify(dataList);
        const data = JSON.parse(unparsed_data);

        var routes = [];

        var allroads = [];
        
        var numroutes = data.length;

        for(let i=0; i<numroutes; i++) {
            var coordinates = data[i].routes;
            var roads = ['abc', '123']; //data[i].roads;

            //converting coordinates = ["(x1,y1)", "(x2,y2)" ...] to coordinates = [[x1, y1], [x2, y2] ...]
            coordinates = coordinates.map(coord => {
                coord = coord.slice(1, -1);
                return coord.split(',').map(Number);
            });

            allroads.push(roads);

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

            //sets variables to respective received values fetched from response
            var risk_val = data[i].risk;
            var traveltime_val = data[i].traveltime;
            var distance_val = data[i].distance;
            var color = getRandomColor();
            
            //draws the rotues given the coordinates (polyline from leaflet map library)
            var route = L.polyline(coordinates, {color: color, weight: 6, opacity: 1});
            routes.push(route);
            routes[i].addTo(results_map);
            
            //inputs new values into results table and changes values
            if(results_value_table) {
                var newRow = results_value_table.insertRow();
                var routeNumberCell = newRow.insertCell();
                var riskCell = newRow.insertCell();
                var traveltimeCell = newRow.insertCell();
                var distanceCell = newRow.insertCell();
                var colorCell = newRow.insertCell();
        
                routeNumberCell.textContent = i + 1;
                riskCell.textContent = risk_val;
                traveltimeCell.textContent = traveltime_val.toFixed(0); 
                distanceCell.textContent = distance_val.toFixed(0);
                
                //selective div for the color mini box for each route path in the table
                var colorDiv = document.createElement('div');
                colorDiv.style.width = '20px';
                colorDiv.style.height = '20px'; 
                colorDiv.style.backgroundColor = color;
                colorDiv.style.border = '1px solid black';
                colorDiv.style.cursor = 'pointer';

                //gets appropriate index and row
                (function(index, row) {
                    temproads = allroads[index];
                    colorDiv.addEventListener('click', function () {
                        if (routes[index].options.opacity === 0) {
                            routes[index].setStyle({ opacity: 1 });
                            routes[index].setStyle({ pointerEvents: 'auto' });
                            row.style.background = '#00000000';
                            allroads[index] = temproads;
                        } else {
                            routes[index].setStyle({ opacity: 0 });
                            routes[index].setStyle({ pointerEvents: 'none' });
                            row.style.background = '#85858575';
                            allroads[index] = [];
                            console.log(allroads);
                        }
                        let roadscontent = '(ROUTE #). (ROADS JOURNEYED)\n';
                        allroads.forEach((roadlist, index) => {
                            if(allroads[index].length != 0) {
                                let roadsublist = roadlist.join(', ');
                                roadscontent += `${index + 1}. ${roadsublist}<br>`
                            }
                        })
                        road_display.innerHTML = roadscontent;
                    });
                })(i, newRow);
        
                colorCell.appendChild(colorDiv);
            }
            let roadscontent = '';
            allroads.forEach((roadlist, index) => {
                if(allroads[index] != []) {
                    let roadsublist = roadlist.join(', ');
                    roadscontent += `${index + 1}. ${roadsublist}<br>`
                }
            })
            road_display.innerHTML = roadscontent;
        }
    })
}

//runs functions on load page
Submit_Prefences();
Submit_All();

//for map resizing to fix poor initial loader
setTimeout(function () {
    window.dispatchEvent(new Event("resize"));
 }, 500);
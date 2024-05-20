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

var results_value_table = document.getElementById('values-table-component');

//fetch api data
async function load_api() {
    const response = await fetch('frontend/js/test.geojson', {method: 'GET'}); //set fetch URL (currently it is a json file and is temporary)
    const data = await response.json();
    var numroutes = data.length;

    for(let i=0; i<numroutes; i++){
        var coordinates = data[i].routes;
        var risk_val = data[i].risk;
        var traveltime_val = data[i].traveltime;
        var distance_val = data[i].distance;
        var color = getRandomColor()
        var route = L.polyline(coordinates, {color: color, weight: 2.75, opacity: 1});
        route.addTo(results_map);

        var newRow = results_value_table.insertRow();
        var routeNumberCell = newRow.insertCell();
        var riskCell = newRow.insertCell();
        var traveltimeCell = newRow.insertCell();
        var distanceCell = newRow.insertCell();
        var colorCell = newRow.insertCell();

        routeNumberCell.textContent = i + 1;
        riskCell.textContent = risk_val;
        traveltimeCell.textContent = traveltime_val; 
        distanceCell.textContent = distance_val;

        var colorDiv = document.createElement('div');
        colorDiv.style.width = '20px';
        colorDiv.style.height = '20px'; 
        colorDiv.style.backgroundColor = color;
        colorDiv.style.border = '1px solid black';

        colorCell.appendChild(colorDiv);
        
        

    }
}
load_api();

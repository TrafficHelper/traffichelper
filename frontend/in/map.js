var map = L.map('map', {
    center: [43.00, -79.00],
    zoom: 15
}).setView([45.424721, -75.695000], 12);

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20
}).addTo(map);

function fetch_pathways_GeoJSON() {
    return fetch('./openottawa/path_network_api.geojson')
        .then(response => response.json());
}

// Load the GeoJSON (skeleton city)
fetch_pathways_GeoJSON()
    .then(geojson => {
        L.geoJSON(geojson, {
        style: function (feature) {
            return {
            color: '#fac402',
            weight: 0.75,
            opacity: 1
            };
        }
        }).addTo(map);
    })
    .catch(error => {
        console.error('Error getting GeoJSON:', error);
});

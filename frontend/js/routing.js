const center = {
    lat: 45.424721,
    lng: -75.695000,
};

var start_pos;
var end_pos;

const setstart_button = document.getElementById('set-start-button');
const setend_button = document.getElementById('set-end-button');

const starting_address = document.getElementById('starting-address');
const ending_address = document.getElementById('ending-address');

const start_marker = L.marker(center, {
    draggable: true,
    icon: L.icon({
    iconUrl: 'frontend/assets/icons/start_icon.png',
        iconSize: [30, 50], //[width, height] (px)
        iconAnchor: [15, 50], //point of the icon which will correspond to marker's location
    })
});

const end_marker = L.marker(center, {
    draggable: true,
    icon: L.icon({
        iconUrl: 'frontend/assets/icons/end_icon.png',
        iconSize: [30, 50],
        iconAnchor: [15, 50],
    })
});

//storing initial (default) values to variables in local storage
window.addEventListener("load", (event) => {
    if (!localStorage.getItem("start_point")) localStorage.setItem("start_point", center);
    if (!localStorage.getItem("end_point")) localStorage.setItem("end_point", center);
});

start_marker.addTo(map);

end_marker.addTo(map);

start_marker.on('dragend', function (event) {
    const start_marker = event.target;
    start_pos = start_marker.getLatLng();
});

end_marker.on('dragend', function (event) {
    const end_marker = event.target;
    end_pos = end_marker.getLatLng();
});

setstart_button.addEventListener('click', function() {
    if(starting_address.value) localStorage.setItem("start_point", starting_address.value);
    else localStorage.setItem("start_point", start_pos);
})

setend_button.addEventListener('click', function() {
    if(ending_address.value) localStorage.setItem("end_point", ending_address.value);
    else localStorage.setItem("end_point", end_pos);
})
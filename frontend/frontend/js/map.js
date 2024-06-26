//sets initial theme
localStorage.setItem("maptheme", "dark");

theme = localStorage.getItem("maptheme");

//initializes map (from leaflet)
var map = L.map('map', {
    center: [43.00, -79.00],
    zoom: 15
}).setView([45.424721, -75.695000], 12);

if(theme == "dark"){
    //adds tilelayer to map
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>',
        maxZoom: 20,
    }).addTo(map);
} else {
    //adds tilelayer to map
    L.tileLayer('    https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>',
        maxZoom: 20,
    }).addTo(map);
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
        L.tileLayer('    https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>',
            maxZoom: 20,
        }).addTo(map);
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
        }).addTo(map);
        //sets initial theme
        localStorage.setItem("maptheme", "dark");
        change_theme_button.style.background = "#ffffff";
        moon.style.boxShadow = "0.35rem 0.35rem 0 0 #191919";
    }
});

//storing initial (default) values to variables in local storage
window.addEventListener("load", (event) => {
    console.log("adding");
    if (!localStorage.getItem("budget_value")) localStorage.setItem("budget_value", "");
    if (!localStorage.getItem("lane_check")) localStorage.setItem("lane_check", "false");
    if (!localStorage.getItem("speed_increase_check")) localStorage.setItem("speed_increase_check", "false");
    if (!localStorage.getItem("stoplight_check")) localStorage.setItem("stoplight_check", "false");
    if (!localStorage.getItem("camera_check")) localStorage.setItem("camera_check", "false");
    console.log("added");
});

const setbudget_input = document.getElementById("budget-input");

const lane_mark = document.getElementById("lane");
const speed_increase_mark = document.getElementById("speed-increase");
const stoplight_mark = document.getElementById("spotlight");
const camera_mark = document.getElementById("camera");

const submit_form_button = document.getElementById("submit-admin-queries-button");
const admin_results = document.getElementById("admin-specific-results");

setbudget_input.value = localStorage.getItem("budget_value");
setbudget_input.addEventListener('change', function(event) {
    localStorage.setItem("budget_value", setbudget_input.value);
});

lane_mark.checked = localStorage.getItem("lane_check");
lane_mark.addEventListener('change', function(event) {
    localStorage.setItem("lane_check", lane_mark.checked);
});

speed_increase_mark.checked = localStorage.getItem("speed_increase_check");
speed_increase_mark.addEventListener('change', function(event) {
    localStorage.setItem("speed_increase_check", speed_increase_mark.checked);
});

stoplight_mark.checked = localStorage.getItem("stoplight_check");
stoplight_mark.addEventListener('change', function(event) {
    localStorage.setItem("stoplight_check", stoplight_mark.checked);
});

camera_mark.checked = localStorage.getItem("camera_check");
camera_mark.addEventListener('change', function(event) {
    localStorage.setItem("camera_check", camera_mark.checked);
});

const admin_url = 'http://127.0.0.1:8000/'; //add correct URL

function Submit_Admin() {
    var budget_value = localStorage.getItem("budget_value");
    var lane_check = localStorage.getItem("lane_check");
    var speed_increase_check = localStorage.getItem("speed_increase_check");
    var stoplight_check = localStorage.getItem("stoplight_check");
    var camera_check = localStorage.getItem("camera_check");

    let formData = {
        "budget": parseInt(budget_value),
        "GadgetRestrictions": {
            "lane": lane_check,
            "speed_increase": speed_increase_check,
            "stoplight": stoplight_check,
            "camera": camera_check
        }
    }

    fetch(admin_url, {
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
        
        admin_results.innerHTML = data; //fix...
    })
}

submit_form_button.addEventListener('click', function() {
    Submit_Admin();
    console.log("ok");
})

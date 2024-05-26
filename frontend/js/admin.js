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

// const setbudget_input = document.getElementById("budget-input");

// const lane_mark = document.getElementById("lane");
// const speed_increase_mark = document.getElementById("speed-increase");
// const stoplight_mark = document.getElementById("spotlight");
// const camera_mark = document.getElementById("camera");

// const submit_form_button = document.getElementById("submit-admin-queries-button");
// const admin_results = document.getElementById("admin-specific-results");

// setbudget_input.value = localStorage.getItem("budget_value");
// setbudget_input.addEventListener('change', function(event) {
//     localStorage.setItem("budget_value", setbudget_input.value);
// });

// lane_mark.checked = localStorage.getItem("lane_check");
// lane_mark.addEventListener('change', function(event) {
//     localStorage.setItem("lane_check", lane_mark.checked);
// });

// speed_increase_mark.checked = localStorage.getItem("speed_increase_check");
// speed_increase_mark.addEventListener('change', function(event) {
//     localStorage.setItem("speed_increase_check", speed_increase_mark.checked);
// });

// stoplight_mark.checked = localStorage.getItem("stoplight_check");
// stoplight_mark.addEventListener('change', function(event) {
//     localStorage.setItem("stoplight_check", stoplight_mark.checked);
// });

// camera_mark.checked = localStorage.getItem("camera_check");
// camera_mark.addEventListener('change', function(event) {
//     localStorage.setItem("camera_check", camera_mark.checked);
// });

// const admin_url = 'https://api.openai.com/v1/chat/completions'; //add correct URL

var csvData = null;
// const file = '/Users/matthewzhou/Desktop/traffichelper/backend_and_api/src/backend/Data/TrafficCollisionData.csv';
// Papa.parse(file, {
//     complete: function (results) {
//         console.log("CSV parsing results:", results);
//         csvData = results.data;
//     }
// });

fetch('/backend_and_api/src/backend/Data/Traffic_Collision_Data_small.csv')
    .then(response => response.text())
    .then(csvText => {
        Papa.parse(csvText, {
            complete: function (results) {
                console.log("CSV parsing results:", results);
                csvData = results.data;
            }
        });
    })
    .catch(error => console.error('Error fetching CSV file:', error));

async function submitQuestionForAi() {
    const askAIInput = document.getElementById('ai-input');
    const resultOutput = document.getElementById('admin-specific-results'); // Get the textarea element
    const prompt = "Given the following data: " + JSON.stringify(csvData) + ", in roughly 60 words answer my question, which is " + askAIInput.value;
    const url = 'https://api.openai.com/v1/chat/completions' // Replace with url of desired formatter
    const api_access_key = 'sk-proj-1soxFYxzZdFWNv18BcbwT3BlbkFJ08m9aBiI5ZMpWjlxFqjF' // Enter your API key here
   
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+ api_access_key
            },
            body: JSON.stringify({
                "model": "gpt-3.5-turbo-0125", // You can set your model here
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a road safety planner with the City of Ottawa in Canada."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens: 150
            })
        });

        const dataList = await response.json();
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }

        // Set the result in the textarea
        resultOutput.value = dataList.choices[0].message.content;
        console.log('Success:', dataList);

    } catch (error) {
        console.error('Error:', error);
        // Display an error message in the textarea
        resultOutput.value = 'Error: ' + error.message;
    }

}
document.getElementById('submit-admin-queries-button').addEventListener('click', submitQuestionForAi);

// submit_form_button.addEventListener('click', function() {
//     Submit_Admin();
//     console.log("ok");
// })

//traffic data path: 
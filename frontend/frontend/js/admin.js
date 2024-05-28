//storing initial (default) values to variables in local storage
window.addEventListener("load", (event) => {
    //if statements to check if item exists already in localStorage; if not, set to default
    if (!localStorage.getItem("budget_value")) localStorage.setItem("budget_value", "");
    if (!localStorage.getItem("lane_check")) localStorage.setItem("lane_check", "out");
    if (!localStorage.getItem("speed_increase_check")) localStorage.setItem("speed_increase_check", "out");
    if (!localStorage.getItem("stoplight_check")) localStorage.setItem("stoplight_check", "out");
    if (!localStorage.getItem("camera_check")) localStorage.setItem("camera_check", "false");
});

//html element for budget input
const setbudget_input = document.getElementById("budget-input");
//html element(s) for gadget restriction inputs
const lane_mark = document.getElementById("lane");
const speed_increase_mark = document.getElementById("speed-increase");
const stoplight_mark = document.getElementById("stoplight");
const camera_mark = document.getElementById("camera");
//html element for submit admin form button
const submit_form_button = document.getElementById("submit-admin-queries-button");
//html element for results logging box
const admin_results = document.getElementById("admin-specific-results");

//gets budget_value from local storage and sets to html element
setbudget_input.value = localStorage.getItem("budget_value");
//listens for input change and sets localStorage stored to new
setbudget_input.addEventListener('change', function(event) {
    localStorage.setItem("budget_value", setbudget_input.value);
});

//gets lane_mark from local storage and sets to html element
if (localStorage.getItem("lane_check") == "") lane_mark.checked = true;
else lane_mark.checked = false;
//listens for input change and sets localStorage stored to new
lane_mark.addEventListener('change', function(event) {
    if(lane_mark.checked == true) localStorage.setItem("lane_check", "");
    else localStorage.setItem("lane_check", "out");
});

//gets speed_increase_check from local storage and sets to html element
if (localStorage.getItem("speed_increase_check") == "") speed_increase_mark.checked = true;
else speed_increase_mark.checked = false;
//listens for input change and sets localStorage stored to new
speed_increase_mark.addEventListener('change', function(event) {
    if(speed_increase_mark.checked == true) localStorage.setItem("speed_increase_check", "");
    else localStorage.setItem("speed_increase_check", "out");
});

//gets stoplight_check from local storage and sets to html element
if (localStorage.getItem("stoplight_check") == "") stoplight_mark.checked = true;
else stoplight_mark.checked = false;
//listens for input change and sets localStorage stored to new
stoplight_mark.addEventListener('change', function(event) {
    if(stoplight_mark.checked == true) localStorage.setItem("stoplight_check", "");
    else localStorage.setItem("stoplight_check", "out");
});

//gets camera_check from local storage and sets to html element
if (localStorage.getItem("camera_check") == "") camera_mark.checked = true;
else camera_mark.checked = false;
//listens for input change and sets localStorage stored to new
camera_mark.addEventListener('change', function(event) {
    if(camera_mark.checked == true) localStorage.setItem("camera_check", "");
    else localStorage.setItem("camera_check", "out");
});

//initializes csv data file
var csvData = null;

//parses csv file  ==> tokens required for much larger files, smaller version is used here instead
fetch('/frontend/js/Traffic_Collision_Data_small.csv')
    .then(response => response.text())
    .then(csvText => {
        Papa.parse(csvText, {
            complete: function (results) {
                console.log("CSV parsing results:", results);
                csvData = results.data;
            }
        });
    })
    //catches errors and console.logs
    .catch(error => console.error('Error fetching CSV file:', error));

/**
 * Submits question and performs json fetch POST and GET methods to OpenAI API
 * @param none
 * @return none
 */
async function submitQuestionForAi() {
    const within_budget = "budget less than " + localStorage.getItem("budget_value") + ", ";
    const gadget_restrictions = "with" + localStorage.getItem("lane_check") + " LANE permitted with" + localStorage.getItem("speed_increase_check") + " SPEED_INCREASE permitted with" + localStorage.getItem("stoplight_check") + " STOPLIGHT permitted with" + localStorage.getItem("camera_check") + " CAMERA permitted";
    const response_length = "within " + 60 + " words, ";
    const askAIInput = document.getElementById('ai-input');
    const resultOutput = document.getElementById('admin-specific-results'); // Get the textarea element
    const prompt = "Given the following data: " + JSON.stringify(csvData) + ", answer my question " + response_length + "and under the constraints of " + gadget_restrictions + ", and with a " + within_budget + askAIInput.value;
    const url = 'https://api.openai.com/v1/chat/completions'; // Replace with url of desired formatter
    const api_access_key = 'sk-proj-hhYDwl5apYRBtki64Aa0T3BlbkFJ8VDOv1DLB67I99tLm3ou'; // Enter your API key here **given here, however later on it is important to replace with one unique to you**
   
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+ api_access_key
            },
            body: JSON.stringify({
                "model": "gpt-3.5-turbo", // You can set your model here
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

//listens for submit_form_button element to be clicked
submit_form_button.addEventListener('click', function() {
    //on click, submitQuestoinForAi()
    submitQuestionForAi();
})

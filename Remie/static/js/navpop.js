function sideClick() {
    $(document).ready(function () {
        $('#sidebar').toggleClass('active');
    });
}

function bot_response() {
    $(document).ready(function () {
        $('.bot_mouth').css('animation-name', 'mouthtalk');
    });
}

function bot_listen(button) {
    var player = document.getElementById("music");
    player.classList.toggle("paused");
    if (player.classList.contains("paused")) {
        // Start listening
        startSpeechRecognition();
    } else {
        // Stop listening
        stopSpeechRecognition();
    }
}

function startSpeechRecognition() {
    const recognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
    if (typeof recognition !== "undefined") {
        const recognitionInstance = new recognition();
        recognitionInstance.continuous = true;
        recognitionInstance.interimResults = true;
        recognitionInstance.addEventListener("result", onResult);
        recognitionInstance.start();
    } else {
        console.log("Speech recognition is not supported in this browser.");
    }
}

function stopSpeechRecognition() {
    const recognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
    if (typeof recognition !== "undefined") {
        const recognitionInstance = new recognition();
        recognitionInstance.stop();
    }
}

function onResult(event) {
    const speechResult = event.results[event.results.length - 1][0].transcript;
    sendrequest(speechResult);
}

function sendrequest(text_message) {
    // Create form structure to populate and send to API
    const formData = new FormData();

    // Populate form
    formData.append("text_message", text_message);

    // Async fetch POST request to API
    fetch("/api", {
        method: "POST",
        body: formData
    })
    .then(function(response) {
        if (!response.ok) {
            throw new Error("Network response was not ok.");
        }
        return response.json();
    })
    .then(function(response) {
        console.log("Response from API:", response);

        // Handle the response from the Chat GPT model
        const assistantResponse = response;
        if ('speechSynthesis' in window) {
            // Speech Synthesis is supported
            const utterance = new SpeechSynthesisUtterance(assistantResponse);
            speechSynthesis.speak(utterance);
        } else {
            // Speech Synthesis is not Supported 
            console.log("Speech synthesis isn't supported in this browser.");
        }
    })
    .catch(function(error) {
        console.error("Error in async fetch:", error);
    });
}

// Add any other JavaScript functions or logic as needed.

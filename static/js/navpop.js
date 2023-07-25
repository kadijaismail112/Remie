
// function sideClick() {
//    $(document).ready(function () {
//        $('#sidebar').toggleClass('active');
//    });
// }

// function bot_response() {
//    $(document).ready(function () {
//        $('.bot_mouth').css('animation-name', 'mouthtalk');
//    });
// }

// function bot_listen(button) {
//    var player = document.getElementById("music");
//    player.classList.toggle("paused");

<<<<<<< HEAD
//    // Get the user input from the text field
//    var userInput = document.querySelector("input[name=dash_input]").value;

//    // Create a FormData object to send the user input to the backend
//    var formData = new FormData();
//    formData.append("text_message", userInput);

//    // Send a POST request to the Chat GPT API endpoint
//    fetch("/api", {
//        method: "POST",
//        body: formData
//    })
//    .then(function(response) {
//        // Handle the response from the API
//        if (response.ok) {
//            return response.json();
//        } else {
//            throw new Error("Network response was not ok.");
//        }
//    })
//    .then(function(data) {
//        // Display the response from the Chat GPT API in the conversation list
//        const conversationList = document.getElementById("conversation");
//        const userMessageItem = document.createElement("li");
//        userMessageItem.textContent = `User: ${userInput}`;
//        conversationList.appendChild(userMessageItem);

//        const assistantMessageItem = document.createElement("li");
//        assistantMessageItem.textContent = `Assistant: ${data.assistant_response}`;
//        conversationList.appendChild(assistantMessageItem);

=======
function bot_listen(button) {
    window.addEventListener("DOMContentLoaded", () => {
        const button = document.getElementById("button");
        const main = document.getElementsByTagName("main")[0];
        let arr =[]
        let listening = false;


        const SpeechRecognition =
          window.SpeechRecognition || window.webkitSpeechRecognition;
        if (typeof SpeechRecognition !== "undefined") {
          const recognition = new SpeechRecognition();

          const stop = () => {
            main.classList.remove("speaking");
            recognition.stop();
            // send ajax request of arr to server to be processed by chatgpt
            sendrequest(arr.join(""))
            // reset the text array that we used to track our speech
            arr = []
            button.textContent = "Start listening";
          };

          const start = () => {
            main.classList.add("speaking");
            recognition.start();
            button.textContent = "Stop listening";
          };

          const onResult = event => {
            for (const res of event.results) {
              let s = ""
              
              if (res.isFinal) {
                // we only track speech to text when speech is finalized   
                s=res[0].transcript
                arr.push(s)
              }
            }
          };
          recognition.continuous = true;
          recognition.interimResults = true;
          recognition.addEventListener("result", onResult);
          button.addEventListener("click", event => {
            listening ? stop() : start();
            listening = !listening;
          });
        } else {
          button.remove();
          const message = document.getElementById("message");
          message.removeAttribute("hidden");
          message.setAttribute("aria-hidden", "false");
        }

        function sendrequest (text_message){
            // Create form structure to populate and send to API
            let formData = new FormData();

            // Populate form
            formData.append("text_message", text_message);

            // Documentation: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
            // Async fetch POST request to API
            fetch("/api", {
            method: "POST",
            body: formData
            })
            .then(function(response) {
                // This right here is the response we will receive before we convert
                // it over to readable JSON
                console.log("Response turning to readable JSON", response);
                return response.json();
            })
            .then(function(response) {
                // Don't worry if this says "false", it just returns that when the user already exists from flasks end
                // Once it reaches here, the async is already successful
                console.log("Successful async: ", JSON.stringify(response));

                // REF: https://www.educative.io/answers/how-to-convert-text-to-speech-in-javascript
                if ('speechSynthesis' in window) {
                // Speech Synthesis is supported 🎉
                let utterance = new SpeechSynthesisUtterance(response);
                speechSynthesis.speak(utterance);
                }else{
                // Speech Synthesis is not Supported 😞 
                console.log("speech synthesis isn't supported")
                }

            })
            .catch(function(error) {
                console.log("Error in async", error);
            });
        }


      });
//    var player = document.getElementById("music");
//    player.classList.toggle("paused");

//    // Get the user input from the text field
//    var userInput = document.querySelector("input[name=dash_input]").value;

//    // Create a FormData object to send the user input to the backend
//    var formData = new FormData();
//    formData.append("text_message", userInput);

//    // Send a POST request to the Chat GPT API endpoint
//    fetch("/api", {
//        method: "POST",
//        body: formData
//    })
//    .then(function(response) {
//        // Handle the response from the API
//        if (response.ok) {
//            return response.json();
//        } else {
//            throw new Error("Network response was not ok.");
//        }
//    })
//    .then(function(data) {
//        // Display the response from the Chat GPT API in the conversation list
//        const conversationList = document.getElementById("conversation");
//        const userMessageItem = document.createElement("li");
//        userMessageItem.textContent = `User: ${userInput}`;
//        conversationList.appendChild(userMessageItem);

//        const assistantMessageItem = document.createElement("li");
//        assistantMessageItem.textContent = `Assistant: ${data.assistant_response}`;
//        conversationList.appendChild(assistantMessageItem);

>>>>>>> 12970d4 (trying to figure things out)
//        // Speak the assistant response using speech synthesis
//        if ('speechSynthesis' in window) {
//            let utterance = new SpeechSynthesisUtterance(data.assistant_response);
//            speechSynthesis.speak(utterance);
//        } else {
//            console.log("speech synthesis isn't supported");
//        }
//    })
//    .catch(function(error) {
//        console.log("Error in async", error);
//    });
<<<<<<< HEAD
// }
=======
}
>>>>>>> 12970d4 (trying to figure things out)



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

   // Get the user input from the text field
   var userInput = document.querySelector("input[name=dash_input]").value;

   // Create a FormData object to send the user input to the backend
   var formData = new FormData();
   formData.append("text_message", userInput);

   // Send a POST request to the Chat GPT API endpoint
   fetch("/api", {
       method: "POST",
       body: formData
   })
   .then(function(response) {
       // Handle the response from the API
       if (response.ok) {
           return response.json();
       } else {
           throw new Error("Network response was not ok.");
       }
   })
   .then(function(data) {
       // Display the response from the Chat GPT API in the conversation list
       const conversationList = document.getElementById("conversation");
       const userMessageItem = document.createElement("li");
       userMessageItem.textContent = `User: ${userInput}`;
       conversationList.appendChild(userMessageItem);

       const assistantMessageItem = document.createElement("li");
       assistantMessageItem.textContent = `Assistant: ${data.assistant_response}`;
       conversationList.appendChild(assistantMessageItem);

       // Speak the assistant response using speech synthesis
       if ('speechSynthesis' in window) {
           let utterance = new SpeechSynthesisUtterance(data.assistant_response);
           speechSynthesis.speak(utterance);
       } else {
           console.log("speech synthesis isn't supported");
       }
   })
   .catch(function(error) {
       console.log("Error in async", error);
   });
}

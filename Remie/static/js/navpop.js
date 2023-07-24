

function sideClick(){
    $(document).ready(function () {
       $('#sidebar').toggleClass('active');
    });
  }
  function bot_response(){
   $(document).ready(function () {
      $('.bot_mouth').css('animation-name', 'mouthtalk');
   });
}
function bot_listen(button){
   var player = document.getElementById("music");
   player.classList.toggle("paused");
}
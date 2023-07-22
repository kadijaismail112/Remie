

function sideClick(){
  $(document).ready(function () {
     $('#sidebar').toggleClass('active');
  });
}

let popupWindow;

function openPopup() {
  // Specify the URL of your website
  const url = '/index'; // Replace '/index' with the actual URL of your website

  // Specify the features of the popup window (width and height set directly)
  const windowFeatures = 'width=593,height=711,resizable=no,scrollbars=no,status=no,toolbar=no';

  // Open the popup window
  popupWindow = window.open(url, '_blank', windowFeatures);

  // Add an event listener for the 'resize' event on the opened window
  popupWindow.addEventListener('resize', () => {
    // Reset the window size to the original fixed size
    popupWindow.resizeTo(593, 711);
  });
}
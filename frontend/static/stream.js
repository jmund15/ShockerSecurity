
let fullscreenButton;
let videoContainer;
let streamImage;
let liveIcon;

document.addEventListener('DOMContentLoaded', () => {
    // Select the fullscreen button
    fullscreenButton = document.querySelector('.fullscreen-button');
    videoContainer = document.querySelector('.video-container');
    // Select the image and the live icon elements
    streamImage = document.getElementById('stream-image');
    liveIcon = document.querySelector('.live-icon');

    // Add an event listener for the fullscreen button
    fullscreenButton.addEventListener('click', function () {
        if (document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement) {
            // If in full-screen mode, exit full-screen
            exitFullScreen();
            fullscreenButton.textContent = "Full-screen"; // Change button text
            fullscreenButton.classList.remove('fullscreen-active'); // Remove active class
        } else {
            // If not in full-screen, enter full-screen
            enterFullScreen();
            fullscreenButton.textContent = "Exit Full-screen"; // Change button text
            fullscreenButton.classList.add('fullscreen-active'); // Add active class
        }
    });

    // Add event listeners for image load and error
    streamImage.addEventListener('error', onStreamFail); // Trigger if the image fails to load
    streamImage.addEventListener('load', onStreamSuccess);  // Trigger if the image loads successfully
    // Optionally, you can handle the initial state in case the image is already loading or failed on page load
    if (streamImage.naturalWidth === 0) {
        onStreamFail();
    }
});


// Function to enter full-screen mode
function enterFullScreen() {
    if (videoContainer.requestFullscreen) {
        videoContainer.requestFullscreen();
    } else if (videoContainer.mozRequestFullScreen) { // Firefox
        videoContainer.mozRequestFullScreen();
    } else if (videoContainer.webkitRequestFullscreen) { // Chrome/Safari
        videoContainer.webkitRequestFullscreen();
    } else if (videoContainer.msRequestFullscreen) { // IE/Edge
        videoContainer.msRequestFullscreen();
    }
    
    // After entering fullscreen, force the container to maintain 4:3 aspect ratio
    //videoContainer.style.width = '100vw'; // Full width of viewport
    //videoContainer.style.height = '75vw'; // 4:3 aspect ratio (height = 3/4 * width)
}

// Function to exit full-screen mode
function exitFullScreen() {
    if (document.exitFullscreen) {
        document.exitFullscreen();
    } else if (document.mozCancelFullScreen) { // Firefox
        document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) { // Chrome/Safari
        document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) { // IE/Edge
        document.msExitFullscreen();
    }
}

// Function to show the "LIVE" icon if the image fails to load
function onStreamSuccess() {
    liveIcon.style.display = 'block'; // Show the "LIVE" icon
    fullscreenButton.style.display = 'block';
}

// Function to hide the "LIVE" icon when the image loads successfully
function onStreamFail() {
    liveIcon.style.display = 'none'; // Hide the "LIVE" icon
    fullscreenButton.style.display = 'none';
}

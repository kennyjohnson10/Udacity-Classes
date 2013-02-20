


setup = function() {
	var body = document.getElementById('body');
	var canvas = document.createElement('canvas');

	var context = canvas.getContext('2d');
	
	canvas.width = window.innerWidth;
	canvas.height = window.innerHeight;

	body.appendChild(canvas);

	// Create a new image with a src of "/media/js/standalone/libs/gamedev_assets/ralphyrobot.png" and onload of onImageLoad
	// YOUR CODE HERE
	var image = new Image();

	image.onload = onImageLoad();

	image.src = "/media/js/standalone/libs/gamedev_assets/ralphyrobot.png";
};

onImageLoad = function(){
	// Use the console.log function to print a statement to the browser console.
	// This will print once the image has been downloaded.
	// YOUR CODE HERE
	console.log('Image done loading.');
};

setup();


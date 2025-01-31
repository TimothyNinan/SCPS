async function detectAndCrop() {
  // Load the model using TensorFlow.js AutoML Object Detection
  console.log('Loading model...');
  //wait for 2 seconds
  await new Promise(resolve => setTimeout(resolve, 2000));
  const modelPath = document.getElementById('model-path').innerText;
  console.log('Model path:', modelPath);
  const model = await tf.automl.loadObjectDetection(modelPath); 
   
  // Get the element from static/images/Cars3.png
  const img = document.getElementById('license-plate-image');

  // Options for the detection (adjust score threshold and IOU as needed)
  const options = {
    score: 0.7,  // Only consider detections with a score above 0.5
    iou: 0.5,    // Intersection over Union threshold for non-max suppression
    topk: 20     // Maximum number of boxes to return
  };

  // Perform detection on the image
  const predictions = await model.detect(img, options);
  console.log('Predictions:', predictions); // For Debug

  // If predictions exist, process the first one (assuming it's the license plate)
  if (predictions && predictions[0]) {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    // Get the actual image dimensions (natural width and height)
    const imgWidth = img.naturalWidth;
    const imgHeight = img.naturalHeight;

    // Get the displayed image dimensions (could be different due to scaling)
    const displayedWidth = img.clientWidth;
    const displayedHeight = img.clientHeight;

    // Calculate the scaling factors
    const scaleX = imgWidth / displayedWidth;
    const scaleY = imgHeight / displayedHeight;

    // Get the first prediction's bounding box, adjusted for scaling
    const { left, top, width: boxWidth, height: boxHeight } = predictions[0].box;
    
    // post request to /detect with the bounding box coordinates and size
    fetch('/detect', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        top: top,
        left: left,
        boxWidth: boxWidth,
        boxHeight: boxHeight
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log('Detection response:', data);
    })
    .catch(error => {
      console.error('Error during detection:', error);
    });

    // Apply scaling to the detected bounding box coordinates and size
    const scaledLeft = left * scaleX;
    const scaledTop = top * scaleY;
    const scaledBoxWidth = boxWidth * scaleX;
    const scaledBoxHeight = boxHeight * scaleY;

    // Log the detected bounding box for debugging
    console.log(`Detected box: left=${scaledLeft}, top=${scaledTop}, width=${scaledBoxWidth}, height=${scaledBoxHeight}`);

    // Set the canvas dimensions to match the cropped area
    canvas.width = scaledBoxWidth;
    canvas.height = scaledBoxHeight;

    // Draw the cropped portion of the image on the canvas
    ctx.drawImage(img, scaledLeft, scaledTop, scaledBoxWidth, scaledBoxHeight, 0, 0, scaledBoxWidth, scaledBoxHeight);
    console.log('Cropped license plate drawn on canvas');

    // save the cropped image to a file
    // canvas.toBlob(function(blob) {
    //   const url = URL.createObjectURL(blob);
    //   const a = document.createElement('a');
    //   a.href = url;
    //   a.download = 'cropped_license_plate.png';
    //   a.click();
    // });
    
  } else {
    console.error('No license plate detected');
  }
}

// Run the function after the page loads
window.onload = () => {
  console.log('Page loaded, starting detection and cropping');
  detectAndCrop();
};

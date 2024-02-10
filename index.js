
// Initialize and add the map
let map;
const San_Diego = { lat: 32.7157, lng: -117.1611 };

/**
 * Creates a control that recenters the map on San Diego.
 */
function createCenterControl(map) {
  const controlButton = document.createElement("button");

  // Set CSS for the control.
  controlButton.style.backgroundColor = "#fff";
  controlButton.style.border = "2px solid #fff";
  controlButton.style.borderRadius = "3px";
  controlButton.style.boxShadow = "0 2px 6px rgba(0,0,0,.3)";
  controlButton.style.color = "rgb(25,25,25)";
  controlButton.style.cursor = "pointer";
  controlButton.style.fontFamily = "Roboto,Arial,sans-serif";
  controlButton.style.fontSize = "16px";
  controlButton.style.lineHeight = "38px";
  controlButton.style.margin = "8px 0 22px";
  controlButton.style.padding = "0 5px";
  controlButton.style.textAlign = "center";
  controlButton.textContent = "Center Map";
  controlButton.title = "Click to recenter the map";
  controlButton.type = "button";
  // Setup the click event listeners: simply set the map to Chicago.
  controlButton.addEventListener("click", () => {
    map.setCenter(San_Diego).zoom(10);
  });
  return controlButton;
}

let rectangles = [];
let areRectanglesVisible = false;

// Function that allows the training squares to appear/reappear upon button click
function toggleTrainingAreas() {
  if (areRectanglesVisible) {
    // Hide the rectangles
    rectangles.forEach(rectangle => rectangle.setMap(null));
  } else {
    if (rectangles.length > 0) {
      // Show the rectangles if they already exist
      rectangles.forEach(rectangle => rectangle.setMap(map));
    } else {
      // Load and create the rectangles if they don't exist
      var training_points = 'training_locations.json';
      d3.json(training_points).then(function(data) {
        data.forEach(element => {
          const rectangle = new google.maps.Rectangle({
            strokeColor: "#FF0000",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            map: map,
            bounds: {
              north: element[2],
              south: element[0],
              east: element[3],
              west: element[1],
            },
          });
          rectangles.push(rectangle);
        });
      });
    }
  }
  // Toggle the visibility state
  areRectanglesVisible = !areRectanglesVisible;
}


/**
 * Creates a button that turns training boxes on/off.
 */
function createTrainingToggle(map) {
  const controlButton = document.createElement("button");

  // Set CSS for the control.
  controlButton.style.backgroundColor = "#fff";
  controlButton.style.border = "2px solid #fff";
  controlButton.style.borderRadius = "3px";
  controlButton.style.boxShadow = "0 2px 6px rgba(0,0,0,.3)";
  controlButton.style.color = "rgb(25,25,25)";
  controlButton.style.cursor = "pointer";
  controlButton.style.fontFamily = "Roboto,Arial,sans-serif";
  controlButton.style.fontSize = "16px";
  controlButton.style.lineHeight = "38px";
  controlButton.style.margin = "8px 0 22px";
  controlButton.style.padding = "0 5px";
  controlButton.style.textAlign = "center";
  controlButton.textContent = "Training Areas";
  controlButton.title = "Click to Turn Training Areas on/off";
  controlButton.type = "button";
  // Setup the click event listeners
  controlButton.addEventListener("click", toggleTrainingAreas);

  return controlButton;
}

/**
 * Creates a button that activates our model.
 */
function createModelExecution(map) {
  const controlButton = document.createElement("button");

  // Set CSS for the control.
  controlButton.style.backgroundColor = "#fff";
  controlButton.style.border = "2px solid #fff";
  controlButton.style.borderRadius = "3px";
  controlButton.style.boxShadow = "0 2px 6px rgba(0,0,0,.3)";
  controlButton.style.color = "rgb(25,25,25)";
  controlButton.style.cursor = "pointer";
  controlButton.style.fontFamily = "Roboto,Arial,sans-serif";
  controlButton.style.fontSize = "16px";
  controlButton.style.lineHeight = "38px";
  controlButton.style.margin = "8px 0 22px";
  controlButton.style.padding = "0 5px";
  controlButton.style.textAlign = "center";
  controlButton.textContent = "Identify Poles";
  controlButton.title = "Click to run model and look for poles";
  controlButton.type = "button";
  // Setup the click event listeners
  //
  return controlButton;
}


// Initializes google map
async function initMap() {
  // The location of San Diego
  const position = { lat: 32.7157, lng: -117.1611 };
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map, centered at San Diego
  map = new Map(document.getElementById("map"), {
    zoom: 12,
    center: position,
    mapId: "satellite",
    scaleControl: true,
    //mapTypeControl: false
  });

  // Create a div to display the zoom level
  const zoomControlDiv = document.createElement("div");
  updateZoomControl(zoomControlDiv, map.getZoom());
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(zoomControlDiv);

  // Listen for zoom changes to update the control
  map.addListener("zoom_changed", () => {
    updateZoomControl(zoomControlDiv, map.getZoom());
  });
  
  // Function to update the zoom level control
  function updateZoomControl(controlDiv, zoomLevel) {
    controlDiv.innerHTML = `<div style="background-color: white; padding: 5px; border: 1px solid black; margin: 10px;">Zoom Level: ${zoomLevel}</div>`;
  }
  
  //Button for centering on San Diego
  {
    // Create the DIV to hold the control for centering
    const centerControlDiv = document.createElement("div");
    // Create the control.
    const centerControl = createCenterControl(map);
    // Append the control to the DIV.
    centerControlDiv.appendChild(centerControl);
    map.controls[google.maps.ControlPosition.LEFT_TOP].push(centerControlDiv);
  }

  // Button for turning training areas on/off
  {
    // Create the DIV
    const trainingBoxesDiv = document.createElement("div");
    // Create the control
    const trainingBoxes = createTrainingToggle(map)
    // Append the control
    trainingBoxesDiv.appendChild(trainingBoxes)
    map.controls[google.maps.ControlPosition.LEFT_TOP].push(trainingBoxesDiv);
  }

  // Button for applying our model
  {
    // Create the DIV
    const runModelDiv = document.createElement("div");
    // Create the control
    const runModel = createModelExecution(map)
    // Append the control
    runModelDiv.append(runModel)
    map.controls[google.maps.ControlPosition.LEFT_TOP].push(runModelDiv)
  }

}

initMap();
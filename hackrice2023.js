
let flightGraph;

function preload() {
  flightGraph = loadGraphFromJSON();
}


function setup() {
  createCanvas(800, 600);
  
  /*
  let boy = { thing1: func => boy.thing2 = "a", thing2: true };
  delete boy.thing2
  
  if (boy.thing1) {
    print("One")
  }
  if (boy.thing2) {
    print("Two")
  }
  */
  
  noLoop();
}


function draw() {
  background(128 * sin(millis()/1000), 64, 64);
  drawEdges();
  drawNodes();
}


function loadGraphFromJSON() {
  // Takes the JSON file outputted by the Python side of things and turns it into workable objects
  graph_json = loadJSON("graph.json");
  return graph_json;
}


function coordsToScreenPos(pos) {
  // Extremes of USA:  
  // maine: 44.807, -68.828
  // maimi: 25.795, -80.290
  // san diego: 32.734, -117.190
  // portland: 45.589, -122.597
  
  // have to switch x and y for some reason
  
  // x (was y) range: -130 to -60 <-- 70 * (0<1) - 130 ==> ((-130<-60) + 130) / 70
  // y (was x) range: 20 to 50 <-- 30 * (0<1) + 20 ==> ((20<50) - 20) / 30
  
  // Screen goes from 0, 0 to width, height
  return [width * (pos[1] + 126) / 60, height * (1.0 - (pos[0] - 20) / 30 + 0.05)];
}


function drawUSA() {
  
}


function drawNodes() {
  noStroke();
  fill(255,0,0);
  for (let a = 0; a < Object.keys(flightGraph).length; a++) {
    let thisKey = Object.keys(flightGraph)[a];
    let thisAirport = flightGraph[thisKey];
    let aScreenCoords = coordsToScreenPos(thisAirport.coordinates);
    ellipse(aScreenCoords[0], aScreenCoords[1], 5, 5);
  }
}


function drawEdges() {
  stroke(200,255,255,100);
  for (let a = 0; a < Object.keys(flightGraph).length; a++) {
    let thisKey = Object.keys(flightGraph)[a];
    let thisAirport = flightGraph[thisKey];
    let aScreenCoords = coordsToScreenPos(thisAirport.coordinates);
    
    for (let f = 0; f < thisAirport.flights.length; f++) {
      let flight = thisAirport.flights[f];
      let destCode = flight.dest_code;
      let destA = flightGraph[destCode];
      let destScreenCoords = coordsToScreenPos(destA.coordinates);
      
      line(aScreenCoords[0], aScreenCoords[1], destScreenCoords[0], destScreenCoords[1]);
    }
  }
}

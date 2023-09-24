
let flightGraph;
let canva;
let latestPath = null;

function preload() {
  flightGraph = loadGraphFromJSON();
}


function setup() {
  let parentDiv = document.getElementById("main")
  canva = createCanvas(parentDiv.offsetWidth,300);
  canva.parent("main")
  noLoop();
}


function draw() {
  updateCanvasSize();
  fill(0);
  noStroke();
  rect(0,0,width,height);
  drawEdges();
  drawNodes();
  highlightPath();
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


function highlightPath() {
  print(latestPath);
  if (latestPath != null) {
    stroke(255,255,0);
    strokeWeight(2);
    for (let i = 0; i < latestPath.length-1; i++) {
      let currentCoords = flightGraph[latestPath[i]].coordinates;
      let currentScreenCoords = coordsToScreenPos(currentCoords);
      let nextCoords = flightGraph[latestPath[i+1]].coordinates;
      let nextScreenCoords = coordsToScreenPos(nextCoords);
      line(currentScreenCoords[0], currentScreenCoords[1], nextScreenCoords[0], nextScreenCoords[1]);
    }
  }
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
  strokeWeight(1);
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



let logs = []
function get_flight(start_airport,end_airport,carbon_weight,time_weight) {
    carbon_weight = carbon_weight / 100;
    time_weight = time_weight / 100;
    let unvisited = new Set();
    let distances = new Object()
    let paths = new Object()
    let airports = Object.keys(flightGraph)
    
    for (let airport of airports) {
      distances[airport] = Number.POSITIVE_INFINITY;  // Use JavaScript's Infinity
      paths[airport] = [start_airport];
      unvisited.add(airport);
    }

    distances[start_airport] = 0
    
    while (unvisited.size > 0){
        const unvisitedArr = Array.from(unvisited);
        
        const sortedUnvisitedArr = unvisitedArr.sort((a, b) => distances[a] - distances[b]);
        const currentAirport = sortedUnvisitedArr[0];
        if (currentAirport == end_airport){
            console.log("WOOOO");
            // Run function to update map
            latestPath = paths[currentAirport];
            draw();  // need to redraw to display latest path
            return [distances[currentAirport], paths[currentAirport]]
        }
        unvisited.delete(currentAirport)
        currflights = flightGraph[currentAirport].flights
        for (let flight of currflights){
            function calcWeights(curr_flight){
              return curr_flight.duration * Number(time_weight) + curr_flight.carbon * Number(carbon_weight)
            }
            console.log(flight)
            console.log(distances[currentAirport], calcWeights(flight), distances[flight.dest_code])
            if (distances[currentAirport] + calcWeights(flight) < distances[flight.dest_code]){
                distances[currentAirport] + calcWeights(flight) < distances[flight.dest_code];
                distances[flight.dest_code] = distances[currentAirport] + calcWeights(flight)
                paths[flight.dest_code] = paths[currentAirport].concat([flight.dest_code])
            }
        }
    }
    console.log("not pog")
    return "no flight path found"
}


function onClick() {
  // Called when the form's submit button is clicked
    let start_airport = document.getElementById("sport").value;
    if (start_airport.length < 4) {
        start_airport = "K" + start_airport;
        document.getElementById("sport").value = "K" + document.getElementById("sport").value;
    }
    let end_airport = document.getElementById("eport").value;
    if (end_airport.length < 4) {
        end_airport = "K" + end_airport;
        document.getElementById("eport").value = "K" + document.getElementById("eport").value;
    }
    let carbon_weight = Number(document.getElementById("cweight").value);
    let time_weight = Number(document.getElementById("tweight").value);
    document.getElementById("stuff").innerHTML = get_flight(start_airport,end_airport,carbon_weight,time_weight);
}


function updateCanvasSize() {
  // Works
  let canvasDiv = document.getElementById('main');
  if (width != canvasDiv.offsetWidth || height != canvasDiv.offsetHeight) {
    resizeCanvas(canvasDiv.offsetWidth * 0.9, canvasDiv.offsetHeight);
  }
}


function fitToContainer(canvas){
  // Seems to doesn't works
  // Make it visually fill the positioned parent
  canvas.style.width ='100%';
  canvas.style.height='100%';
  // ...then set the internal size to match
  canvas.width = canvas.offsetWidth * 0.9;
  canvas.height = canvas.offsetHeight * 0.9;
}


function windowResized() {
  // called when window is resized
  updateCanvasSize();
  draw();
}

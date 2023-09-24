
let flightGraph;
let canva;

function preload() {
  flightGraph = loadGraphFromJSON();
}


function setup() {
  let parentDiv = document.getElementById("main")
  canva = createCanvas(parentDiv.offsetWidth,400);
  canva.parent("main")

  //fitToContainer(canva);
  
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
  //noLoop();
}


function draw() {
  background(128 * sin(millis()/1000), 64, 64);
  //drawEdges();
  //drawNodes();
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

function get_flight(start_airport,end_airport,carbon_weight,time_weight) {
    let unvisited = new Set();
    let distances = new Object()
    let paths = new Object()
    let airports = Object.keys(flightGraph)

    for (airport in airports){
        distances[airport] = 1.797693134862315E+310
        paths[airport] = [start_airport]
        unvisited.add(airport)
    }

    distances[airport] = 0

    while (unvisited.size > 0){
        let currentAirport = Array.from(unvisited).sort(function(a,b){distances[a] > distances[b]})[0]
        if (currentAirport == end_airport){
            return(distances[currentAirport], paths[currentAirport])
        }
        unvisited.delete(currentAirport)

        for (flight in currentAirport.flights){
            function calcWeights(curr_flight){
                curr_flight.duration * Number(time_weight) + curr_flight.carbon * Number(carbon_weight)
            }
            if (distances[currentAirport] + calcWeights(flight) < distances[flight.dest_code]){
                distances[flight.dest_code] = distances[currAirport] + calc_weights(flight)
                paths[flight.dest_code] = paths[currAirport] + [flight.dest_code]
            }
        }
    }
    return "no flight path found"
}
function onClick(){
    let start_airport = document.getElementById("sport").value
    let end_airport = document.getElementById("eport").value
    let carbon_weight = Number(document.getElementById("cweight").value)
    let time_weight = Number(document.getElementById("tweight").value)
    document.getElementById("sport").innerHTML = get_flight(start_airport,end_airport,carbon_weight,time_weight)
}
function updateCanvasSize() {
  let canvasDiv = document.getElementById('canvasContainer');
  if (width != canvasDiv.offsetWidth || height != canvasDiv.offsetHeight) {
    resizeCanvas(canvasDiv.offsetWidth, canvasDiv.offsetHeight);
  }
}


function fitToContainer(canvas){
  // Make it visually fill the positioned parent
  canvas.style.width ='100%';
  canvas.style.height='100%';
  // ...then set the internal size to match
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
  print("canvas fitted to container");
  print(canvas.style.width);
}

/*
function windowResized() {
  // called when window is resized
  fitToContainer(canva);
}
*/
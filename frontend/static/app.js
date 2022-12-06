//Set elements from HTML file
let read_img_button = document.getElementById("read_image");
let read_midi_button = document.getElementById("read_midi");

let img_result = document.getElementById("img_result");
let midi_result = document.getElementById("midi_result");

// file reader for the image
const reader = new FileReader();

// Add event listener to run naive bayes function
read_img_button.addEventListener("click", convertToXML);
read_midi_button.addEventListener("click", generateMore);

// event listener for reader load event
function handleFileRead(event) {
  //event.preventDefault();
  if (event.type === "load") {
    // create an image element and add it to the webpage
    // this will only be called when reader.result has been loaded
    console.log("file loaded");
    //send image to backend (preps, processes, returns xml)
    fetch("/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ img_src: reader.result }),
    })
      .then((response) => response.json())
      .then(function (data) {
        console.log("GET response:");
        let file_link = data["file_url"];
        console.log(file_link);
        //adds link to download file, link appears on screen and when clicked downloads an xml to the computer
        let link = document.createElement("a");
        link.setAttribute("download", "");
        //link.href = "static/note_image/test.png";
        link.href = file_link;
        link.innerHTML = "download musicxml file";
        link.className = "btn btn-secondary";
        img_result.append(link);
        img_result.append(document.createElement("br"));
        img_result.append(document.createElement("br"));
        let image = document.createElement("img");
        image.src = reader.result;
        img_result.append(image);
      });
  }
}

// Called to run the backend
// Loads the image and converts it to an xml file
function convertToXML() {
  //read image
  //event.preventDefault();
  let file = document.getElementById("upload_image").files[0];
  console.log(file);
  if (file) {
    reader.addEventListener("load", handleFileRead);
    // the event listener will be loaded

    reader.readAsDataURL(file);
  }
}

function generateMore() {
  //read image
  //event.preventDefault();
  let file = document.getElementById("upload_midi").files[0];
  console.log(file);
  if (file) {
    reader.addEventListener("load", handleMidiRead);
    // the event listener will be loaded

    reader.readAsDataURL(file);
  }
}

function handleMidiRead(event) {
  //event.preventDefault();
  if (event.type === "load") {
    // this will only be called when reader.result has been loaded
    console.log("file loaded");
    //send midi file to backend and composes more then returns output midi
    fetch("/midiupload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ file_data: reader.result }),
    })
      .then((response) => response.json())
      .then(function (data) {
        console.log("GET response:");
        let file_link = data["file_url"];
        console.log(file_link);
        //adds link to download file, link appears on screen and when clicked downloads the generated midi
        let link = document.createElement("a");
        link.className = "btn btn-secondary";
        link.setAttribute("download", "");
        link.href = file_link;
        link.innerHTML = "download generated midi file";
        midi_result.append(link);
      });
  }
}

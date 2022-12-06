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
    let loader = document.createElement("div");
    loader.className = "spinner-border";
    loader.setAttribute("role", "status");
    img_result.append(loader);
    let time_signature = document.getElementById("time_signature").value;
    //send image to backend (preps, processes, returns xml)
    fetch("/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        img_src: reader.result,
        time_sig: time_signature,
      }),
    })
      .then((response) => response.json())
      .then(function (data) {
        console.log("GET response:");
        img_result.removeChild(loader);
        read_img_button.removeAttribute("disabled", "");
        let file_link = data["file_url"];
        console.log(file_link);
        //adds link to download file, link appears on screen and when clicked downloads an xml to the computer
        let link = document.createElement("a");
        link.setAttribute("download", "");
        //link.href = "static/note_image/test.png";
        link.href = file_link;
        link.innerHTML =
          '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/></svg> Download musicxml';
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
  if (img_result.hasChildNodes()) {
    img_result.innerHTML = "";
  }
  let file = document.getElementById("upload_image").files[0];
  read_img_button.setAttribute("disabled", "");
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
  if (midi_result.hasChildNodes()) {
    midi_result.innerHTML = "";
  }
  let file = document.getElementById("upload_midi").files[0];
  read_midi_button.setAttribute("disabled", "");
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
    let loader = document.createElement("div");
    loader.className = "spinner-border";
    loader.setAttribute("role", "status");
    midi_result.append(loader);
    //send midi file to backend and composes more then returns output midi
    fetch("/midiupload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ file_data: reader.result }),
    })
      .then((response) => response.json())
      .then(function (data) {
        midi_result.removeChild(loader);
        console.log("GET response:");
        let file_link = data["file_url"];
        console.log(file_link);
        //adds link to download file, link appears on screen and when clicked downloads the generated midi
        let link = document.createElement("a");
        link.className = "btn btn-secondary";
        link.setAttribute("download", "");
        link.href = file_link;
        link.innerHTML =
          '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-download" viewBox="0 0 16 16"><path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"/><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"/></svg> Download generated midi';
        midi_result.append(link);
        read_midi_button.removeAttribute("disabled", "");
      });
  }
}

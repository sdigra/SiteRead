//Set elements from HTML file
let read_img_button = document.getElementById("read_image");

let document_contets = document.getElementById("result");

// file reader for the image
const reader = new FileReader();

// Add event listener to run naive bayes function
read_img_button.addEventListener("click", convertToXML);

// event listener for reader load event
function handleEvent(event) {
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
      .catch(console.log("Error occured"))
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
        document_contets.append(link);
        let image = document.createElement("img");
        image.src = reader.result;
        document_contets.append(image);
      });
  }
}

// Called to run the backend
// Loads the image and converts it to an xml file
function convertToXML(event) {
  //read image
  //event.preventDefault();
  let file = document.getElementById("upload_image").files[0];
  console.log(file);
  if (file) {
    reader.addEventListener("load", handleEvent);
    // the event listener will be loaded

    reader.readAsDataURL(file);
  }
}
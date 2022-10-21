//Set elements from HTML file
let read_img_button = document.getElementById("read_image");

let document_contets = document.getElementById("result");

// Add event listener to run naive bayes function
read_img_button.addEventListener("click", convertToXML);
let img_upload = document.getElementById("read_image");

// Called to run the backend
// Loads the image and converts it to an xml file
function convertToXML() {
  //read image
  let file = document.getElementById("upload_image").files[0];
  console.log(file);
  let reader = new FileReader();
  reader.readAsArrayBuffer(file);
  //let image = document.createElement("p");
  console.log(reader.result);
  //document_contets.append(image);

  //send image to backend (preps, processes, returns xml)

  //adds link to download file, link appears on screen and when clicked downloads an xml to the computer
  let link = document.createElement("a");
  link.href = "../AlgorithmicExample.musicxml";
  link.setAttribute("download", "");
  link.innerHTML = "download xml file";
  document_contets.append(link);
}

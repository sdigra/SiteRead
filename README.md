# SiteRead

## Introduction

Welcome to SiteRead!

SiteRead is an application to convert an image of printed or handwritten sheet music into a file compatible with online sheet music editors. Most sheet music editing software, for example musescore, allow an upload of a musicxml file, so SiteRead returns a musicxml file. Additionally, you can upload a midi file to our generator feature and a midi file will be returned matching the key and general feeling of the original piece.

Currently, no such application exists that we are aware of to convert handwritten sheetmusic to a digital format. The lack of many comprehensive data sets has limited the development of similar applications. We got this idea because two members of our group are musicians who are frustrated that they can't easily convert their physical music into a digital format without using a music editing software to manually add all the notes.

## Technical Architecture

Our application was made with HTML, CSS, JavaScript and Python.

The front end is made with HTML, CSS and JavaScript and uses Bootstrap stylization.

The user uploads an image of sheet music and it is passed to the back end where it is processed and converted into an xml file. A Naive Bayes algorithm is then used to read each note and find the beats associated with the given note. A musicxml file is then generated and sent back to the front end for the user to download.

The backend is Python and utilizes the numpy and scikit-learn packages for machine learning and note classification.

Below is an explanation of data flow through our application between front end and back end.

![Technical Architecture](TechnicalArchitecture.png)

## Installation Instructions

You can install all our dependencies with

```bash
pip install -r requirements.txt
```

Then, switch into our frontend folder and set up the Flask application.

```bash
cd frontend
export FLASK_APP=main_flask.py
```

To run the application, type

```bash
flask run
```

and open http://127.0.0.1:5000 in your browser of choice.

## Group Roles

Brandon: Worked on the backend, training the machine learning model and classifying notes.

Elvin: Worked on the backend, identifying the key of each note

Siya: Worked on the backend, converting notes classified by the model to an XML format and converting that to MIDI, and playing the output

Sofia: Worked on designing the frontend and connecting it through flask to the python components the rest of the group worked on.

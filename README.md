# SiteRead

## Introduction

Welcome to SiteRead!

Currently, no such application exists that we are aware of to convert handwritten sheetmusic to a digital format. The lack of many comprehensive data sets has limited the development of similar applications. We got this idea because two members of our group are musicians who are frustrated that they can't easily convert their physical music into a digital format without using a music editing software to manually add all the notes.

## Technical Architecture

Our application was made with HTML, CSS, JavaScript and Python.

The frontend is made with HTML, CSS and JavaScript and uses Bootstrap stylization.

The user uploads an image of sheet music and it is passed to the back end where it is processed and converted into an xml file. A Naive Bayes algorithm is then used to read each note and find the beats associated with the given note. A musicxml file is then generated and sent back to the front end for the user to download.

The backend is Python and utilizes the numpy and scikit-learn packages for machine learning and note classification.
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

Elvin:

Siya: Worked on the backend, converting notes classified by the model to an XML format and converting that to MIDI, and playing the output

Sofia: Worked on designing the front end and connecting it through flask to the python components the rest of the group worked on.

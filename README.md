# SiteRead

## Introduction

Welcome to SiteRead!

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

Siya:

Sofia: worked on designing the front end and connecting it through flask to the python components the rest of the group worked on.

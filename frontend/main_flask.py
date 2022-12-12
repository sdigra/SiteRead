from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import base64
import sys
# sys.path.insert(1, "/Users/siya/UIUC/CS 222/course-project-group-27/export_to_xml.py")
from pycomposer.gancomposable._mxnet.conditional_gan_composer import ConditionalGANComposer
from logging import getLogger, StreamHandler, NullHandler, DEBUG, ERROR
# import mxnet as mx
import torch
import numpy as np
import PIL as Image
from modules import train_model
from modules import parse_sheet
from modules import export_to_xml
from modules import nb_train
# main flask file to run python programs

# https://flask.palletsprojects.com/en/2.2.x/
# can install flask with pip install flask

# terminal commands to run flask app: 
# export FLASK_APP=main_flask.py
# flask run

app = Flask(__name__)
Classifier = train_model.train()
# runs when the app is opened
@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)

# main processsing function, will be called with a JSON holding the image the user uploaded
@app.route('/upload', methods=['GET', 'POST'])
def upload_img():
    if request.method == 'POST':
        content = request.get_json()
        time_signature = content["time_sig"].split("/")
        print(time_signature)
        # meta data and content of image are divided by "," in the passed in array buffer string
        img_data = content["img_src"].split(",")
        print(img_data[0])
        # img holds the data for the image uploaded by the user
        img = base64.b64decode(img_data[1])

        # write image to file, used for tesing, 
        # can do this when implemented if easier to process
        with open('static/result_files/test.png', 'wb') as f:
              f.write(img)
        # process image here
        note_images = parse_sheet.sheet_to_notes('static/result_files/test.png', 8, 4)
        notes_no_lines = parse_sheet.remove_lines(note_images)
        notes = Classifier.predict(notes_no_lines)

        keys = [0 for i in notes]
        count = 0
        for i in notes:
            keys[count] = nb_train.get_key(np.asarray(note_images[count]))
            count += 1
        export_to_xml.generate_from_input(notes, keys)
        
        print(notes)
        print(keys)
        # return xml file which should be stored in the result_files folder 
        # or else there will be problems downloading it
        # when the xml is returned only the file path needs to be returned 
        # with the key 'file_url' in the dictionary/JSON d
        d = {'file_url': "static/result_files/InputGenerated.musicxml"}
        return d

@app.route('/midiupload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        content = request.get_json()
        midi_data = content["file_data"].split(",")
        mid = base64.b64decode(midi_data[1])
        # write image to file, used for tesing, 
        # can do this when implemented if easier to process
        with open('input.mid', 'wb') as f:
              f.write(mid)
        # generate more here 

        ctx = "cuda:0" if torch.cuda.is_available() else "cpu"

        logger = getLogger("pygan")
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        logger.setLevel(DEBUG)
        logger.addHandler(handler)

        composer = ConditionalGANComposer(midi_path_list=[f.name], 
                                          batch_size = 1,
                                          seq_len = 100,
                                          learning_rate = 0.0002,
                                          time_fraction = 0.25,
                                          ctx = mx.gpu())

        composer.learn(iter_n=1000, k_step=10)

        composer.compose(
            file_path="static/result_files/output.mid", 
            # Mean of velocity.
            # This class samples the velocity from a Gaussian distribution of 
            # `velocity_mean` and `velocity_std`.
            # If `None`, the average velocity in MIDI files set to this parameter.
            velocity_mean=30,
            # Standard deviation(SD) of velocity.
            # This class samples the velocity from a Gaussian distribution of 
            # `velocity_mean` and `velocity_std`.
            # If `None`, the SD of velocity in MIDI files set to this parameter.
            velocity_std=0
        )
        # return midi file
        d = {'file_url': "/static/result_files/output.mid"}
        return d

if __name__ == '__main__':
   app.run()



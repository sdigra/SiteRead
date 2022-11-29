from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import base64, os

# main flask file to run python programs
#might need to move frontend over to react for better integration with flask

# https://flask.palletsprojects.com/en/2.2.x/
# can install flask with pip install flask

# terminal commands to run flask app: 
# export FLASK_APP=main_flask.py
# flask run

app = Flask(__name__)

# runs when the app is opened
@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)

# main processsing function, will be called with a JSON holding the image the user uploaded
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        content = request.get_json()
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

        # return xml file which should be stored in the result_files folder 
        # or else there will be problems downloading it
        # when the xml is returned only the file path needs to be returned 
        # with the key 'file_url' in the dictionary/JSON d
        d = {'file_url': f.name}
        return d
    return "file successfully uploaded"

if __name__ == '__main__':
   app.run()



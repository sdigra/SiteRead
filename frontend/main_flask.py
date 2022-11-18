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

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        content = request.get_json()
        #print(content)
        # meta data and content of image are divided by "," in the passed in array buffer string
        img_data = content["img_src"].split(",")
        print(img_data[0])
        decoded = base64.b64decode(img_data[1])

        #write image to file, used for tesing
        with open(os.path.abspath('./static/xml_files/test.png'), 'wb') as f:
              f.write(decoded)

        d = {'file_url': "/Users/sofiasivilotti/Documents/course-project-group-27/frontend/xml_files/AlgorithmicExample1.musicxml"}
        return d
    # print(file)
    # uploaded_file = request.files['upload_image']
    # print(uploaded_file.filename)
    # if uploaded_file.filename != '':
    #     uploaded_file.save(uploaded_file.filename)
    #     # redirect(url_for('index'))
    return "file successfully uploaded"

if __name__ == '__main__':
   app.run()



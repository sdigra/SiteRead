from flask import Flask, render_template, request, redirect, url_for

# main flask file to run python programs
#might need to move frontend over to react for better integration with flask

# https://flask.palletsprojects.com/en/2.2.x/
# can install flask with pip install flask

app = Flask(__name__)

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    content = request.get_json(force=True)
    print(content)
    if request.method == 'POST':
        #print(request.get_json()['file'])  # parse as JSON
        d = {'file_url': "../AlgorithmicExample.musicxml"}
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



from flask import Flask, render_template, request, redirect, url_for

# main flask file to run python programs
#might need to move frontend over to react for better integration with flask

# https://flask.palletsprojects.com/en/2.2.x/
# can install flask with pip install flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['upload_image']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return redirect(url_for('index'))

if __name__ == '__main__':
   app.run()



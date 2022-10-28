from flask import Flask, render_template

# main flask file to run python programs
#might need to move frontend over to react for better integration with flask

# https://flask.palletsprojects.com/en/2.2.x/
# can install flask with pip install flask

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)


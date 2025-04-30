
from flask import Flask, request, render_template
import os
from parser.parse_resume import parse_and_score

import os

UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['resume']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            score, feedback = parse_and_score(filepath)
            return render_template('index.html', score=score, feedback=feedback)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

# Source: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

import os
import uuid

#from flask import Flask, flash, request, redirect, url_for, render_template
from flask import *
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/files'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def retrieveFiles():
    entries = os.listdir(app.config['UPLOAD_FOLDER'])
    fileList = []
    for entry in entries:
        fileList.append(entry)
    return fileList

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # added uuid to make the filename unique. Otherwise, file with same names will override.
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()) + filename))

            return render_template('home.html', fileList=retrieveFiles())


    return render_template('home.html', fileList=retrieveFiles())


if __name__ == '__main__':
    app.run()

import os
from app import app
from flask import flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from ocr import ocr_text
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
from wand.image import Image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No file selected for uploading!')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # print('upload_image filename: ' + filename)
        text = ocr_text(filename)
        return render_template('upload.html', filename=filename, text=text)
    else:
        flash('Allowed image types are -> png, jpg, jpeg')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.run(port=port)

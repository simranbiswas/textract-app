import os
from app import app
from flask import flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from ocr import ocr_text
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

ALLOWED_EXTEN = set(['pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_pdf(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTEN

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

    elif file and allowed_pdf(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        images = convert_from_path(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(images)
        images[0].save(os.path.join(app.config['UPLOAD_FOLDER'], str(filename) + '.jpg'))
        img_path = str(filename) +'.jpg'
        '''
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        images = convert_from_path(file_path)
        temp_images = []
        for i in range(len(images)):
            # images[i].save('sample' + str(i) + '.jpg')
            images[i].save(os.path.join(app.config['UPLOAD_FOLDER'], str(filename) + str(i) + '.jpg'))
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], str(filename) + str(i) + '.jpg')
            temp_images.append(img_path)

        imgs = list(map(Image.open, temp_images))
        print(imgs)
        print("####")
        try:
            min_img_width = min(i.width for i in imgs)
        except:
            min_img_width = imgs[0].width
        print(min_img_width)
        # find total height of all images
        total_height = 0
        for i, img in enumerate(imgs):
            total_height += imgs[i].height
        # create new image object with width and total height
        merged_image = Image.new(imgs[0].mode, (min_img_width, total_height))
        # paste images together one by one
        y = 0
        for img in imgs:
            merged_image.paste(img, (0, y))
            y += img.height

        merged_image.save(os.path.join(app.config['UPLOAD_FOLDER'], str(filename) + '.jpg'))
        '''
        text = ocr_text(img_path)
        return render_template('upload.html', filename=img_path, text=text)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.run(port=port)

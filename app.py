from io import BytesIO
from flask import Flask, render_template, request, send_file
from image_downloader import ImageDownloader
from image_editor import ImageResizer
from csv_reader import CSVReader
from PIL import Image
import os
from pathlib import Path

def create_folders():
    folders = [Path('images','fullsize'),Path('images','wallpapers'),Path('static','banner')]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

create_folders()

app = Flask(__name__)
downloader = ImageDownloader()
reader = CSVReader()

def get_combined_image_info():
    image_names = downloader.img_names
    banner_paths = downloader.banner_paths
    combined = zip(image_names, banner_paths)
    return combined

def get_supported_smartphones():
    return reader.get_display_names()

@app.route('/')
@app.route('/index')
def index():
    combined = get_combined_image_info()
    display_names = get_supported_smartphones()
    return render_template('index.html', images=combined, display_names=display_names)

@app.route('/get_image', methods=['POST'])
def get_image():
    form = request.form
    selected_image = None if form['gallery-radio'] == 'gallery' else form['gallery-radio']
    phone = None if form['phone'] == '' else form['phone']
    width = None if form['width'] == '' else int(form['width'])
    height = None if form['height'] == '' else int(form['height'])
    wide_image = request.form.get('wide-image') == 'on'
    
    if phone is not None:
        target_width, target_height = reader.get_phone_resolution(phone)
    elif height is not None:
        target_width, target_height = width, height
    else:
        return 'Error: No phone or resolution specified', 406
        
    if wide_image:
        target_width = None

    if selected_image is not None:
        image_path = downloader.get_image(selected_image)
    else:
        return 'Error: No image selected', 406

    resizer = ImageResizer(Image.open(image_path), target_height, target_width)
    resized = resizer.resize().convert('RGB')
    image_io = BytesIO()
    resized.save(image_io, 'JPEG', quality=95)
    image_io.seek(0)
    return send_file(image_io, mimetype='image/jpeg', as_attachment=True, attachment_filename=f'{selected_image}.jpg')

if __name__ == '__main__':
    Flask.run(app, debug=True, host='0.0.0.0', port=8080)
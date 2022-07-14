from flask import Flask, render_template, request
from sympy import true
from image_downloader import ImageDownloader
from image_editor import ImageResizer
from csv_reader import CSVReader
from pathlib import Path
from PIL import Image

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
    #print(form['phone'], form['width'], form['height'], form['wide-image'], form['gallery-radio'])
    selected_image = form['gallery-radio']
    phone = None if form['phone'] == '' else form['phone']
    width = None if form['width'] == '' else int(form['width'])
    height = None if form['width'] == '' else int(form['width'])
    wide_image = True if form['wide-image'] == 'on' else False
    
    if phone is None:
        target_width, target_height = width, height
    else:
        target_width, target_height = reader.get_phone_resolution(phone)

    if wide_image:
        target_width = None

    image_path = Path('images', 'fullsize', selected_image + '.tif')
    resizer = ImageResizer(Image.open(image_path), target_height, target_width)
    wallpaper = resizer.resize()
    
    return 'success'

if __name__ == '__main__':
    Flask.run(app, debug=True)
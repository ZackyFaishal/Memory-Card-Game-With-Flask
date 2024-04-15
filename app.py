import numpy as np
from PIL import Image
import image_processing
import image_game
import os
from flask import Flask, render_template, request, make_response, redirect, url_for, session
from datetime import datetime
from functools import wraps, update_wrapper
from shutil import copyfile

app = Flask(__name__)
app.secret_key = 'secret_key'
# Folder untuk menyimpan gambar yang diunggah
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Pastikan baris ini ada

PROCESSED_FOLDER = 'processed_images'
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

image_pairs = []

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view)


@app.route("/index")
@app.route("/")
@nocache
def index():
    return render_template("home.html", file_path="img/image_here.jpg")


@app.route("/about")
@nocache
def about():
    return render_template('about.html')


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route("/upload", methods=["POST"])
@nocache
def upload():
    target = os.path.join(APP_ROOT, "static/img")
    if not os.path.isdir(target):
        if os.name == 'nt':
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/img_now.jpg")
    copyfile("static/img/img_now.jpg", "static/img/img_normal.jpg")
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/games", methods=["POST"])
def games():
    image_game.game()
    image_paths = [f"static/img/img_{i}.jpg" for i in range(14)]  # Buat daftar path gambar
    return render_template("game.html", file_paths=image_paths)  # Kirim daftar path gambar ke template HTML
    
@app.route('/play_game')
def play_game():
    if len(image_pairs) == 0:
        return "Upload gambar terlebih dahulu untuk memulai permainan."

    session['score'] = 0
    max_score = len(image_pairs) // 2  # Menyimpan nilai maksimum yang akan digunakan di template
    return render_template('game.html', image_pairs=image_pairs, max_score=max_score)



@app.route("/normal", methods=["POST"])
@nocache
def normal():
    copyfile("static/img/img_normal.jpg", "static/img/img_now.jpg")
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/grayscale", methods=["POST"])
@nocache
def grayscale():
    image_processing.grayscale()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/zoomin", methods=["POST"])
@nocache
def zoomin():
    image_processing.zoomin()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/zoomout", methods=["POST"])
@nocache
def zoomout():
    image_processing.zoomout()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_left", methods=["POST"])
@nocache
def move_left():
    image_processing.move_left()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_right", methods=["POST"])
@nocache
def move_right():
    image_processing.move_right()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_up", methods=["POST"])
@nocache
def move_up():
    image_processing.move_up()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/move_down", methods=["POST"])
@nocache
def move_down():
    image_processing.move_down()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_addition", methods=["POST"])
@nocache
def brightness_addition():
    image_processing.brightness_addition()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_substraction", methods=["POST"])
@nocache
def brightness_substraction():
    image_processing.brightness_substraction()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_multiplication", methods=["POST"])
@nocache
def brightness_multiplication():
    image_processing.brightness_multiplication()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/brightness_division", methods=["POST"])
@nocache
def brightness_division():
    image_processing.brightness_division()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/histogram_equalizer", methods=["POST"])
@nocache
def histogram_equalizer():
    image_processing.histogram_equalizer()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/edge_detection", methods=["POST"])
@nocache
def edge_detection():
    image_processing.edge_detection()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/blur", methods=["POST"])
@nocache
def blur():
    image_processing.blur()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/sharpening", methods=["POST"])
@nocache
def sharpening():
    image_processing.sharpening()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/histogram_rgb", methods=["POST"])
@nocache
def histogram_rgb():
    image_processing.histogram_rgb()
    if image_processing.is_grey_scale("static/img/img_now.jpg"):
        return render_template("histogram.html", file_paths=["img/grey_histogram.jpg"])
    else:
        return render_template("histogram.html", file_paths=["img/red_histogram.jpg", "img/green_histogram.jpg", "img/blue_histogram.jpg"])


@app.route("/thresholding", methods=["POST"])
@nocache
def thresholding():
    lower_thres = int(request.form['lower_thres'])
    upper_thres = int(request.form['upper_thres'])
    image_processing.threshold(lower_thres, upper_thres)
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/crop_biasa", methods=["POST"])
def crop_biasa():
    num_puzzles = int(request.form['number_crop'])
    image_path = "static/img/img_now.jpg"  # Assuming this is the path of your uploaded image
    rows = num_puzzles
    cols = num_puzzles

    parts = image_processing.crop_biasa(rows)

    if parts is not None:
        return render_template("crop.html", image_paths=[f"static/img/potongan/img_now_{i}_{j}.jpg" for i in range(rows) for j in range(cols)], rows=rows, cols=cols)
    else:
        return "Terjadi kesalahan saat membagi gambar. Silakan coba lagi." 
    

@app.route("/puzzle", methods=["POST"])
def puzzle():
    num_puzzles = int(request.form['number_crop'])
    image_path = "static/img/img_now.jpg"  # Assuming this is the path of your uploaded image
    rows = num_puzzles
    cols = num_puzzles

    parts = image_processing.crop_biasa(rows)

    if parts is not None:
        return render_template("puzzle.html", image_paths=[f"static/img/potongan/img_now_{i}_{j}.jpg" for i in range(rows) for j in range(cols)], rows=rows, cols=cols)
    else:
        return "Terjadi kesalahan saat membagi gambar. Silakan coba lagi."

@app.route("/puzzle_rgb", methods=["POST"])
@nocache
def puzzle_rgb():
    target = os.path.join(APP_ROOT, "static/img")
    image_dimensions = image_processing.get_image_dimensions("static/img/img_now.jpg")
    rgb_values = image_processing.get_image_rgb("static/img/img_now.jpg")
    if not os.path.isdir(target):
        if os.name == 'nt':
            os.makedirs(target)
        else:
            os.mkdir(target)
    for file in request.files.getlist("file"):
        file.save("static/img/img_now.jpg")
    copyfile("static/img/img_now.jpg", "static/img/img_normal.jpg")
    return render_template("puzzle_rgb.html", file_path="img/img_now.jpg", img_dim=image_dimensions, img_rgb_val=rgb_values)


###########################################################################
@app.route("/identify", methods=["POST"])
@nocache
def identify():
    image_processing.identify()
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/bilateralfilter", methods=["POST"])
@nocache
def bilateralFilter():
    image_processing.bilateralFilter()
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/meanfilter", methods=["POST"])
@nocache
def meanFilter():
    ksize = int(request.form["size-mean"])
    image_processing.meanFilter()
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/blur_filter", methods=["POST"])
@nocache
def blur_filter():
    ksize = int(request.form["blur-filter"])
    image_processing.blur_filter(ksize)
    return render_template("upload.html", file_path="img/img_now.jpg")

@app.route("/sharp", methods=["POST"])
@nocache
def sharp():
    image_processing.sharp()
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/zeropadding", methods=["POST"])
@nocache
def zero_padding():
    image_processing.zeroPadding()
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/medianBlur", methods=["POST"])
@nocache
def medianBlur():
    ksize = int(request.form["size-median"])
    image_processing.medianBlur(ksize)
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/gaussianBlur", methods=["POST"])
@nocache
def gaussianBlur():
    ksize = int(request.form["size-gaussian"])
    image_processing.gaussianBlur(ksize)
    return render_template("uploaded.html", file_path="img/img_now.jpg")

@app.route("/lowpass_filter", methods=["POST"])
@nocache
def lowpass_filter():
    ksize = int(request.form["size-low"])
    image_processing.lowpass_filter(ksize)
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/highpass_filter", methods=["POST"])
@nocache
def highpass_filter():
    ksize = int(request.form["size-high"])
    image_processing.highpass_filter(ksize)
    return render_template("uploaded.html", file_path="img/img_now.jpg")


@app.route("/bandpass_filter", methods=["POST"])
@nocache
def bandpass_filter():
    ksize_low = int(request.form["size-low"])
    ksize_high = int(request.form["size-high"])
    image_processing.bandpass_filter(ksize_low, ksize_high)
    return render_template("uploaded.html", file_path="img/img_now.jpg")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")


import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
import math
from collections import Counter
from pylab import savefig
from skimage import io
import cv2
import os
import random
matplotlib.use("Agg")

def game():
    grayscale()
    zoomin()
    zoomout()
    move_left()
    move_right()
    move_up()
    move_down()
    brightness_addition()
    brightness_substraction()
    brightness_multiplication()
    brightness_division()
    edge_detection()
    blur()
    sharpening()
    

def grayscale():
    if not is_grey_scale("static/img/img_now.jpg"):
        img = Image.open("static/img/img_now.jpg")
        img_arr = np.asarray(img)
        r = img_arr[:, :, 0]
        g = img_arr[:, :, 1]
        b = img_arr[:, :, 2]
        new_arr = r.astype(int) + g.astype(int) + b.astype(int)
        new_arr = (new_arr / 3).astype("uint8")
        new_img = Image.fromarray(new_arr)
        new_img.save("static/img/img_1.jpg")


def is_grey_scale(img_path):
    im = Image.open(img_path).convert("RGB")
    w, h = im.size
    for i in range(w):
        for j in range(h):
            r, g, b = im.getpixel((i, j))
            if r != g != b:
                return False
    return True


def zoomin():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)
    is_gray = is_grey_scale("static/img/img_now.jpg")

    if is_gray:
        new_size = (img_arr.shape[0] * 2, img_arr.shape[1] * 2)
        new_arr = np.full(new_size, 255)
        new_arr.setflags(write=1)

        gray = img_arr[:, :, 0]

        for i in range(new_size[0]):
            for j in range(new_size[1]):
                new_arr[i, j] = gray[i // 2, j // 2]
    else:
        new_size = (img_arr.shape[0] * 2, img_arr.shape[1] * 2, img_arr.shape[2])
        new_arr = np.full(new_size, 255)
        new_arr.setflags(write=1)

        r = img_arr[:, :, 0]
        g = img_arr[:, :, 1]
        b = img_arr[:, :, 2]

        for i in range(new_size[0]):
            for j in range(new_size[1]):
                new_arr[i, j, 0] = r[i // 2, j // 2]
                new_arr[i, j, 1] = g[i // 2, j // 2]
                new_arr[i, j, 2] = b[i // 2, j // 2]

    new_arr = new_arr.astype("uint8")
    new_img = Image.fromarray(new_arr)

    if is_gray:
        new_img = new_img.convert("L")  # Convert back to grayscale
    new_img.save("static/img/img_2.jpg")


def zoomout():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    x, y = img.size
    new_arr = Image.new("RGB", (int(x / 2), int(y / 2)))
    is_gray = is_grey_scale("static/img/img_now.jpg")

    for i in range(0, int(x / 2)):
        for j in range(0, int(y / 2)):
            if is_gray:
                pixel1 = img.getpixel((2 * i, 2 * j))
                pixel2 = img.getpixel((2 * i + 1, 2 * j))
                pixel3 = img.getpixel((2 * i, 2 * j + 1))
                pixel4 = img.getpixel((2 * i + 1, 2 * j + 1))

                avg_r = int((pixel1[0] + pixel2[0] + pixel3[0] + pixel4[0]) / 4)
                avg_g = int((pixel1[1] + pixel2[1] + pixel3[1] + pixel4[1]) / 4)
                avg_b = int((pixel1[2] + pixel2[2] + pixel3[2] + pixel4[2]) / 4)

                new_arr.putpixel((int(i), int(j)), (avg_r, avg_g, avg_b))
            else:
                r = [0, 0, 0, 0]
                g = [0, 0, 0, 0]
                b = [0, 0, 0, 0]

                r[0], g[0], b[0] = img.getpixel((2 * i, 2 * j))
                r[1], g[1], b[1] = img.getpixel((2 * i + 1, 2 * j))
                r[2], g[2], b[2] = img.getpixel((2 * i, 2 * j + 1))
                r[3], g[3], b[3] = img.getpixel((2 * i + 1, 2 * j + 1))

                avg_r = int((r[0] + r[1] + r[2] + r[3]) / 4)
                avg_g = int((g[0] + g[1] + g[2] + g[3]) / 4)
                avg_b = int((b[0] + b[1] + b[2] + b[3]) / 4)

                new_arr.putpixel((int(i), int(j)), (avg_r, avg_g, avg_b))

    new_arr = np.uint8(new_arr)
    new_img = Image.fromarray(new_arr)

    if is_gray:
        new_img = new_img.convert("L")  # Convert back to grayscale
    new_img.save("static/img/img_3.jpg")


def move_left():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale("static/img/img_now.jpg"):
        img_arr = np.pad(img_arr, ((0, 0), (0, 50)), "constant")[:, 50:]
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((0, 0), (0, 50)), "constant")[:, 50:]
        g = np.pad(g, ((0, 0), (0, 50)), "constant")[:, 50:]
        b = np.pad(b, ((0, 0), (0, 50)), "constant")[:, 50:]
        img_arr = np.dstack((r, g, b))

    new_img = Image.fromarray(img_arr)
    new_img.save("static/img/img_4.jpg")


def move_right():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale("static/img/img_now.jpg"):
        img_arr = np.pad(img_arr, ((0, 0), (50, 0)), "constant")[:, :-50]
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((0, 0), (50, 0)), "constant")[:, :-50]
        g = np.pad(g, ((0, 0), (50, 0)), "constant")[:, :-50]
        b = np.pad(b, ((0, 0), (50, 0)), "constant")[:, :-50]
        img_arr = np.dstack((r, g, b))

    new_img = Image.fromarray(img_arr)
    new_img.save("static/img/img_5.jpg")


def move_up():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale("static/img/img_now.jpg"):
        img_arr = np.pad(img_arr, ((0, 50), (0, 0)), "constant")[50:, :]
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((0, 50), (0, 0)), "constant")[50:, :]
        g = np.pad(g, ((0, 50), (0, 0)), "constant")[50:, :]
        b = np.pad(b, ((0, 50), (0, 0)), "constant")[50:, :]
        img_arr = np.dstack((r, g, b))

    new_img = Image.fromarray(img_arr)
    new_img.save("static/img/img_6.jpg")


def move_down():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if is_grey_scale("static/img/img_now.jpg"):
        img_arr = np.pad(img_arr, ((50, 0), (0, 0)), "constant")[0:-50, :]
    else:
        r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
        r = np.pad(r, ((50, 0), (0, 0)), "constant")[0:-50, :]
        g = np.pad(g, ((50, 0), (0, 0)), "constant")[0:-50, :]
        b = np.pad(b, ((50, 0), (0, 0)), "constant")[0:-50, :]
        img_arr = np.dstack((r, g, b))

    new_img = Image.fromarray(img_arr)
    new_img.save("static/img/img_7.jpg")


def brightness_addition():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img).astype("uint16")
    img_arr = img_arr + 100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype("uint8")
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_8.jpg")


def brightness_substraction():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img).astype("int16")
    img_arr = img_arr - 100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype("uint8")
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_9.jpg")


def brightness_multiplication():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    img_arr = img_arr * 1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype("uint8")
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_10.jpg")


def brightness_division():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    img_arr = img_arr / 1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype("uint8")
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_11.jpg")


def convolution(img, kernel):
    if len(img.shape) == 3 and img.shape[2] == 3:  # Color image
        h_img, w_img, _ = img.shape
        out = np.zeros((h_img - 2, w_img - 2), dtype=np.float64)
        new_img = np.zeros((h_img - 2, w_img - 2, 3))
        if np.array_equal((img[:, :, 1], img[:, :, 0]), img[:, :, 2]) == True:
            array = img[:, :, 0]
            for h in range(h_img - 2):
                for w in range(w_img - 2):
                    S = np.multiply(array[h : h + 3, w : w + 3], kernel)
                    out[h, w] = np.sum(S)
            out_ = np.clip(out, 0, 255)
            for channel in range(3):
                new_img[:, :, channel] = out_
        else:
            for channel in range(3):
                array = img[:, :, channel]
                for h in range(h_img - 2):
                    for w in range(w_img - 2):
                        S = np.multiply(array[h : h + 3, w : w + 3], kernel)
                        out[h, w] = np.sum(S)
                out_ = np.clip(out, 0, 255)
                new_img[:, :, channel] = out_
        new_img = np.uint8(new_img)
        return new_img

    elif len(img.shape) == 2:  # Grayscale image
        h_img, w_img = img.shape
        out = np.zeros((h_img - 2, w_img - 2), dtype=np.float64)

        for h in range(h_img - 2):
            for w in range(w_img - 2):
                S = np.multiply(img[h : h + 3, w : w + 3], kernel)
                out[h, w] = np.sum(S)

        out_ = np.clip(out, 0, 255)
        new_img = np.uint8(out_)
        return new_img

    else:
        raise ValueError("Unsupported image format")


def edge_detection():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=int)
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_12.jpg")


def blur():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=int)
    kernel = np.array(
        [[0.0625, 0.125, 0.0625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]]
    )
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_13.jpg")


def sharpening():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=int)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_0.jpg")


def histogram_rgb():
    img_path = "static/img/img_now.jpg"
    img = Image.open(img_path)
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        g = img_arr[:, :].flatten()
        data_g = Counter(g)
        plt.bar(list(data_g.keys()), data_g.values(), color="black")
        plt.savefig(f"static/img/grey_histogram.jpg", dpi=300)
        plt.clf()
    else:
        r = img_arr[:, :, 0].flatten()
        g = img_arr[:, :, 1].flatten()
        b = img_arr[:, :, 2].flatten()
        data_r = Counter(r)
        data_g = Counter(g)
        data_b = Counter(b)
        data_rgb = [data_r, data_g, data_b]
        warna = ["red", "green", "blue"]
        data_hist = list(zip(warna, data_rgb))
        for data in data_hist:
            plt.bar(list(data[1].keys()), data[1].values(), color=f"{data[0]}")
            plt.savefig(f"static/img/{data[0]}_histogram.jpg", dpi=300)
            plt.clf()


def df(img):  # to make a histogram (count distribution frequency)
    values = [0] * 256
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            values[img[i, j]] += 1
    return values


def cdf(hist):  # cumulative distribution frequency
    cdf = [0] * len(hist)  # len(hist) is 256
    cdf[0] = hist[0]
    for i in range(1, len(hist)):
        cdf[i] = cdf[i - 1] + hist[i]
    # Now we normalize the histogram
    # What your function h was doing before
    cdf = [ele * 255 / cdf[-1] for ele in cdf]
    return cdf


def histogram_equalizer():
    img = cv2.imread("static\img\img_now.jpg", 0)
    my_cdf = cdf(df(img))
    # use linear interpolation of cdf to find new pixel values. Scipy alternative exists
    image_equalized = np.interp(img, range(0, 256), my_cdf)
    cv2.imwrite("static/img/img_now.jpg", image_equalized)


def threshold(lower_thres, upper_thres):
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    if not img_arr.flags.writeable:
        img_arr = img_arr.copy()

    condition = np.logical_and(
        np.greater_equal(img_arr, lower_thres), np.less_equal(img_arr, upper_thres)
    )
    print(lower_thres, upper_thres)
    img_arr.setflags(write=1)
    img_arr[condition] = 255
    new_img = Image.fromarray(img_arr)
    new_img.save("static/img/img_now.jpg")
            
def crop_biasa(number_crop):
    # Buka gambar
    image = Image.open('static/img/img_now.jpg')
    img_arr = np.asarray(image)
    file_paths = []

    # Tentukan jumlah baris dan kolom kotak-kotak kecil yang Anda inginkan
    jumlah_baris = number_crop
    jumlah_kolom = number_crop

    # Dapatkan dimensi gambar asli
    width, height = image.size

    # Hitung lebar dan tinggi setiap kotak kecil
    kotak_kecil_lebar = width // jumlah_kolom
    kotak_kecil_tinggi = height // jumlah_baris

    # Pastikan direktori penyimpanan file potongan ada
    os.makedirs('static/img/potongan', exist_ok=True)

    # Loop melalui setiap baris dan kolom untuk memotong gambar
    for i in range(jumlah_baris):
        for j in range(jumlah_kolom):
            left = j * kotak_kecil_lebar
            upper = i * kotak_kecil_tinggi
            right = left + kotak_kecil_lebar
            lower = upper + kotak_kecil_tinggi

            # Potong gambar sesuai dengan kotak kecil saat ini
            cropped_image = image.crop((left, upper, right, lower))

            # Simpan atau tampilkan gambar potongan sesuai kebutuhan
            new_img = Image.fromarray(img_arr)
            new_img_path = f"static/img/potongan/img_now_{i}_{j}.jpg"
            cropped_image.save(new_img_path)
            file_paths.append(new_img_path)
    return file_paths

def get_image_rgb(image_path):
    try:
        with Image.open(image_path) as img:
            rgb_values = list(img.getdata())
            return rgb_values
    except Exception as e:
        return None

def get_image_dimensions(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width, height
    except Exception as e:
        return None

#================================================================================================#


def identify():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=int)
    kernel = np.array([[0, 0, 0],
                    [0, 1, 0],
                    [0, 0, 0]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")

def sharp():
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharp = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    cv2.imwrite("static/img/img_now.jpg", sharp)

def bilateralFilter():
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    bf = cv2.bilateralFilter(src=image,d=9,sigmaColor=75,sigmaSpace=75)
    cv2.imwrite("static/img/img_now.jpg", bf)
    
def zeroPadding():
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    zp = cv2.copyMakeBorder(image, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    cv2.imwrite("static/img/img_now.jpg", zp)
    
def meanFilter(ksize):
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    kernel = np.ones((ksize, ksize), np.float32) / 9
    blur = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    cv2.imwrite("static/img/img_now.jpg", blur)

def gaussianBlur(ksize):
    image = cv2.imread("static/img/img_now.jpg")
    cv_gaussian = cv2.GaussianBlur(image, (ksize, ksize), 0)
    cv2.imwrite("static/img/img_now.jpg", cv_gaussian)

def medianBlur(ksize):
    image = cv2.imread("static/img/img_now.jpg")
    cv_median = cv2.medianBlur(image, ksize)
    cv2.imwrite("static/img/img_now.jpg", cv_median)

def blur_filter(ksize):
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    cv_blur = cv2.blur(src=image, ksize=(ksize,ksize))
    cv2.imwrite("static/img/img_now.jpg", cv_blur)
    
def lowpass_filter(ksize):
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    
    lowFilter = np.ones((ksize,ksize),np.float32)/9
    lowFilterImage = cv2.filter2D(image,-1,lowFilter)
    cv2.imwrite("static/img/img_now.jpg", lowFilterImage)


def highpass_filter(ksize):
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)

    lowFilter = np.ones((ksize, ksize), np.float32) / (ksize * ksize)
    lowFilterImage = cv2.filter2D(image, -1, lowFilter)
    
    highPassImage = image - lowFilterImage
    cv2.imwrite("static/img/img_now.jpg", highPassImage)

def bandpass_filter(ksize_low, ksize_high):
    image_0 = io.imread("static/img/img_now.jpg")
    image = cv2.cvtColor(image_0, cv2.COLOR_BGR2RGB)
    
    lowFilter = np.ones((ksize_low, ksize_low), np.float32) / (ksize_low * ksize_low)
    lowFilterImage = cv2.filter2D(image, -1, lowFilter)
    highFilter = np.ones((ksize_high, ksize_high), np.float32) / (ksize_high * ksize_high)
    highPassImage = image - cv2.filter2D(lowFilterImage, -1, highFilter)
    
    cv2.imwrite("static/img/img_now.jpg", highPassImage)
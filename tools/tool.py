#coding=utf8

import os

from PIL import Image
import numpy as np
import random

def random_rgb():
    """
    随机生成rgb
    """
    r = int(150 * random.random() + 50)
    g = int(150 * random.random() + 50)
    b = int(150 * random.random() + 50)
    return (r, g, b)


def normalize(image):
    image = np.array(image)
    mean = np.mean(image)
    image = image - mean
    maxi = float(np.max(image))
    image = image / maxi
    return image

def load_data_from_imgs(path):
    images = []
    labels = []
    files = os.listdir(path)
    for f in files:
        ln = int(f[0])
        labels.append([1.0 if x == ln else 0.0 for x in range(10)])
        img = Image.open(path + f)
        #images.append([p / 255.0 for p in img.getdata()])
        images.append(normalize(img.getdata()))
    return images, labels

def show_img_from_data(data, size):
    img = Image.new('L', size, '#000')
    for y in range(size[1]):
        for x in range(size[0]):
            img.putpixel((x, y), int(255*data[y*size[0]+x]))
    img.show()

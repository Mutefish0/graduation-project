from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import numpy as np

from PIL import Image

from random import random

images = mnist.train.images
labels = mnist.train.labels
leng = len(labels)

def show(label, n_pictures):
    idx = 0
    while idx < leng:
        skip = int(20 * random())
        idx += skip
        if np.argmax(labels[idx]) == label:
            n_pictures -= 1

            img = Image.new('L', (28, 28), '#000')
            for y in range(28):
                for x in range(28):
                    img.putpixel((x, y), int(255 * images[idx][y * 28 + x]))
            img.show()

            if n_pictures <= 0: return

show(9, 4)

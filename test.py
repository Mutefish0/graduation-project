#coding=utf8
import sys

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

sys.path.append('tools/')
from tool import load_data_from_imgs, show_img_from_data
images, labels  = load_data_from_imgs('correct/')


#100
print mnist.test.labels[200]

show_img_from_data(mnist.test.images[200],(28,28))
show_img_from_data(images[6], (28,28))

#coding=utf8

import tensorflow as tf

x = tf.placeholder("float", [None, 784])
y_ = tf.placeholder("float", [None,10])
# 权重参数
W = tf.Variable(tf.zeros([784, 10]))
# 偏置参数
b = tf.Variable(tf.zeros([10]))

y = tf.nn.softmax(tf.matmul(x, W) + b)

# 取出模型
sess = tf.Session()
saver = tf.train.Saver([W, b])
saver.restore(sess, './model_data/model.ckpt')

# 预测
def predict(images):
    return sess.run(y, {x: images})

###### 正确率测试

# 预测正确性列表 [ True, False, False, True ...]
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
# 正确率
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

# 测试集正确率
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

print "测试集正确率：", sess.run(accuracy, {x: mnist.test.images, y_: mnist.test.labels})

# 矫正集正确率
import sys
sys.path.append('tools/')
from tool import load_data_from_imgs
images, labels  = load_data_from_imgs('correct/')

print "矫正集正确率: ", sess.run(accuracy, {x: images, y_: labels})

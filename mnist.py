#coding=utf8

import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder("float", [None, 784])
# 权重参数
W = tf.Variable(tf.zeros([784, 10]))
# 偏置参数
b = tf.Variable(tf.zeros([10]))


# 预测label
y = tf.nn.softmax(tf.matmul(x, W) + b)
# 实际label
y_ = tf.placeholder("float", [None,10])
# 代价函数: 交叉熵
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
# 梯度下降训练，最小化交叉熵
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

# 初始化变量
init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

# 训练参数1000次。
for i in xrange(1000):
  xs, ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: xs, y_:  ys})

# 预测正确性列表 [ True, False, False, True ...]
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
# 正确率
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))


print "正确率：", sess.run(accuracy, {x: mnist.test.images, y_: mnist.test.labels})


# 存储模型

saver = tf.train.Saver([W, b])
save_path = saver.save(sess, './model_data/model.ckpt')
print 'Model Saved in file:', save_path

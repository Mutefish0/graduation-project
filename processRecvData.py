#coding=utf8

from PIL import Image
import numpy as np

import random

from predict_deep import predict

hex_set = ['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f']

def margin(img, width):
    margined = Image.new('L', map(lambda x: x + 2 * width, img.size), '#000')
    margined.paste(img, (width, width))
    return margined

def cubify(img):
    cubeto = max(img.size)
    cubed = Image.new('L', (cubeto, cubeto), '#000')
    cubed.paste(img, map(lambda x: (cubeto - x) / 2, img.size))
    return cubed

def process(recv):
    width = recv['width']
    height = recv['height']
    data = recv['data']
    correct = recv['correct']

    grey = Image.new('L', (width, height), '#000')
    for y in xrange(height):
        for x in xrange(width):
            grey.putpixel((x, y), data[y][x])

    cubed = cubify(grey)
    cubed = cubed.resize((20, 20), Image.ANTIALIAS)
    mgrey = margin(cubed, 4)

    ## getdata
    #predictData = [p / 255.0 for p in mgrey.getdata()]
    predictData = []
    for y in range(28):
        for x in range(28):
            predictData.append(  mgrey.getpixel((x, y)) / 255.0  )



    labels = predict([predictData])

    if correct:
        mgrey.save(
            './correct/' +
            str(correct) +
            '_' +
            ''.join([random.choice(hex_set) for i in range(8)]) +
            '.png'
        )

    return {
        'number': np.argmax(labels[0]),
        'probs': [round(label * 100, 2) for label in labels[0]]
    }

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


import base64
import cv2

def readb64(base64_string):
    nparr = np.fromstring(base64_string.decode('base64'), np.uint8)
    img = cv2.imdecode(nparr)
    return img

def process_from_img(img_data):
    file_name = './upload_images/' + ''.join([random.choice(hex_set) for i in range(16)]) + '.png'
    with open(file_name, 'wb') as fh:
        fh.write(base64.decodestring(img_data))

    img = cv2.imread(file_name, 0)

    thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,111,20)
    thresh = 255 - thresh
    img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    datas = []
    xIndexs = []
    bdrs = []

    for c in contours:
        if len(c) > 400:
            br = cv2.boundingRect(c)
            bdrs.append(br)
            x,y,w,h = br
            xIndexs.append([x, len(xIndexs)])

            pimg = Image.fromarray(img)
            eimg = pimg.crop((x,y,x+w,y+h))
            cubed = cubify(eimg)
            cubed = cubed.resize((20, 20), Image.ANTIALIAS)
            mgrey = margin(cubed, 4)

            predictData = []
            for y in range(28):
                for x in range(28):
                    predictData.append(  mgrey.getpixel((x, y)) / 255.0  )
            datas.append(predictData)

    labels = predict(datas)
    xIndexs.sort(lambda a,b: a[0] - b[0])
    return {
        'numbers': [np.argmax( labels[idx[1]] ) for idx in xIndexs],
        'boundaries': bdrs
    }

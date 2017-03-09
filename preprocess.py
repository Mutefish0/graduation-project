#coding=utf8

import numpy as np
from PIL import Image, ImageDraw
import sys
sys.path.append('tools')
from tool import binImg2vectors, img2binImg, random_rgb
from sklearn.cluster import KMeans

im = Image.open('./res/B02_E36518_0.jpg')

width, height = im.size

grey = im.convert('L')

vectors = []

for w in xrange(width):
    for h in xrange(height):
        px = grey.getpixel((w, h))
        if(px > 100):
            vectors.append([w, h])

km = KMeans(n_clusters=7, n_init=12)
km.fit(vectors)
means = km.cluster_centers_

draw = ImageDraw.Draw(grey)

"""
for mean in means:
    draw.ellipse([mean[0]-1,mean[1]-1,mean[0]+1,mean[1]+1], fill='skyblue')
"""

means = sorted(means, cmp= lambda x,y: int(x[0]-y[0]))

x1 = int(means[0][0])
x2 = int(means[1][0])
lineWidth = 2
minSum = float('inf')
sump = 0
minX = 0

for x in range(x2)[x1:]:
    sump = 0
    for w in range(x + lineWidth + 1)[x:]:
        for h in xrange(height):
            sump += grey.getpixel((w, h))
    if sump < minSum:
        minSum = sump
        minX = x

draw.line(((minX,0), (minX,height)), 'red')

grey.show()

from PIL import Image
import os
import PIL.ImageOps
from numpy import *
import numpy as np
import random
import matplotlib.pyplot as plt
import time

files = []
for file in os.listdir("paterns"):
    if file.endswith(".png"):
        files.append(file)
images = []
for file in files:
    im = Image.open('paterns/'+file)
    images.append(im)

mim = Image.open('mask02.png')
maskim = 255-asarray(mim)
aim = 255-asarray(im)
bim = asarray(im)

ss = shape(maskim)

background = np.zeros((ss[0],ss[1],3),dtype='uint8')

def imscale(im,scale):
    tim = im.copy()
    size = [int(x*scale) for x in tim.size]
    tim.thumbnail(size)
    return tim


def blit(background,im,x,y):
    w,h,p = shape(im)
    background[x:x+w,y:y+h,:] += im[:,:,0:3]
    return background

#blit(aim,0,0)

def recover(background,im,x,y):
    return _recover(background,im,x,y)+_recover(maskim,im,x,y)


def _recover(background,im,x,y):
    w,h,p = shape(im)
    m = im.sum()
    return (background[x:x+w,y:y+h,1:3] * im[:,:,1:3]).sum()

def loopx(background):
    for x in range(100):
        if recover(background,aim,x,0) == 0:
            print 'does not recover : blit !'
            background = blit(background,aim,x,0)
        else :
            print 'nop'

    return background

def randfill(background,images, step=-5, minsize=0.02):
    fig = plt.figure()
    for i in range(400,10,step):
        time.sleep(0.1)
        scale = (float(i)/800)**2
        image = random.choice(images)
        print 'choice : ',image
        ims = imscale(image, scale)
        #print scale,i,ims
        if scale < minsize :
            break
        ima = 255-asarray(ims)
        print '\n',scale,' : ',
        for j in range( 60):
            xlim = shape(background)[0]-shape(ima)[0]
            ylim = shape(background)[1]-shape(ima)[1]
            x = random.randint(0,xlim)
            y = random.randint(0,ylim)
            if recover(background,ima,x,y) == 0:
                background = blit(background,ima,x,y)
                plt.imshow(255-background)
                fig.canvas.draw()
                #break
                print 'O',
    return background

if __name__ == '__main__':
    pass


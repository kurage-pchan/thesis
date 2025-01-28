import cv2
from matplotlib import pyplot as plt
import numpy as np
from pathlib import Path
import os
import sys
import glob
import time
from PIL import Image

folder_path = "D:/" #絶対パスの指定

path = glob.glob( os.path.join( folder_path, "*.jpg" ) )
print(path) #ここで半角英数字以外がないか確認すること
img = cv2.imread( path[0] )
print( np.array( img ).shape )
data = [ cv2.imread(p,cv2.IMREAD_GRAYSCALE) for p in path ]

cv2.imwrite("output_image3.jpg", data[3])#書き出して正しいデータが入っているか確認


def list_from_mask(images):
    """Convert mask location information to YOLO format

    Parameters
    ----------
    images : ndarray
        taget images

    Returns
    -------
    images_box: list
        List of coordinates converted to YOLO format

    """
    images_box = []
    for img in images:
        img[img<=10]=0
        img[img>10]=255
        imgheight,imgwidth = img.shape[:2]
        _, _, stats, centroids = cv2.connectedComponentsWithStats(255 - img)
        img_box = []

        for i in range(1,len(centroids)):
            x_center = round((centroids[i][0]/imgwidth), 6)
            y_center = round((centroids[i][1]/imgheight), 6)
            width = round((stats[i][2]/imgwidth), 6)
            height = round((stats[i][3]/imgheight), 6)
            img_box.append([1,x_center,y_center,width,height])

        images_box.append(img_box)

    return images_box

def draw_box(images):
    """Display a frame of recognised characters in the image

    Parameters
    ----------
    images : ndarray
        taget images

    Returns
    -------
    stats_show : ndarray
        Image displaying a frame

    """
    print("in function ")
    threshold = 500
    num = 100
    for i, img in enumerate(images):
        img[img<=10]=0
        img[img>10]=255
        img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        _, _, stats, centroids = cv2.connectedComponentsWithStats(255 - img)

        for j in range(1,len(centroids)):
            left_top = (stats[j][0], stats[j][1])
            width = stats[j][2]
            height = stats[j][3]
            if stats[j][4] > threshold:
                right_bottom = (stats[j][0] + width, stats[j][1] + height)
                stats_show = cv2.rectangle(img_color, left_top, right_bottom, (0,255,0), 2)
              
        #出力してファイル書き込み
        cv2.imwrite(os.path.join('./outputtest/img_{}.jpg').format(num), img_color)
        num += 1

images_box = list_from_mask(data)
print(images_box[0][0])
draw_box(data)

#ファイル出力
numb = 100
for i,image in enumerate(images_box):
    path_w = ('./outputtxt/testyolo_{}.txt').format(numb)
    numb += 1

    with open(path_w, mode='w') as f:
        for sub in image:
            f.write(' '.join(map(str, sub)) + '\n')

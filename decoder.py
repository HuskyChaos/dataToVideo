#!/usr/bin/python3
from PIL import Image
import cv2,os

vid = cv2.VideoCapture("./video.avi")
os.system('mkdir pictures')
currentframe = 1
while(True):
    ret,frame = vid.read()
    if ret:
        name = './pictures/frame' + str(currentframe) + '.png'
        cv2.imwrite(name, frame)
        currentframe += 1
    else:
        break
vid.release()
cv2.destroyAllWindows()
exit()
im = Image.open('x.bmp')

imageSizeW, imageSizeH = im.size

nonWhitePixels = []

for i in range(1, imageSizeW):
    for j in range(1, imageSizeH):
        pixVal = im.getpixel((i, j))
        if pixVal != (255, 255, 255):
            nonWhitePixels.append([i, j])

print(nonWhitePixels)
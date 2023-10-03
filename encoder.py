#!/usr/bin/python3
from PIL import Image
import os, subprocess, base64
import numpy as np
try:
    import cv2
except ImportError or ModuleNotFoundError:
    print('[!] CV2 not installed')
    print('[+] Installing CV2')
    cv2 = subprocess.check_output(['pip3', 'install', 'opencv-python'], text=True)
    if "Successfully installed" in cv2:
        print('[+] Successfully installed CV2')
        import cv2
    else:
        print('[!] error')
        quit()

pixels = []
array1 = []
counter1 = 0
counter2 = 0
picnumber = 0
bitCounter = 0

def __createPicture__(j):
    global counter1,counter2,array1,pixels,picnumber
    counter1+=1
    if j == '0':
        array1.append((225, 225, 225))
    elif j == '1':
        array1.append((0, 0, 0))
    if counter1 == 1080:
        pixels.append(array1)
        array1=[]
        counter2+=1
        counter1=0
    if counter2 == 720:
        picnumber+=1
        array = np.array(pixels, dtype=np.uint8)
        new_image = Image.fromarray(array)
        new_image.save(f'pictures/new{picnumber}.png')
        pixels = []
        counter2 = 0

targetFile = open('song.mp3', 'rb')
targetFile = targetFile.read()
b64File = base64.b64encode(targetFile)

fileBits = len((b64File)*7)
count = int(fileBits/(1080*720))
extraBits = fileBits - count * (1080*720)

subprocess.run(['mkdir', 'pictures'])
remainingBits = []
for i in b64File:
    t1 = bin(i)[2:]
    if len(t1) < 7:
        t1 = '0' + t1
    for j in t1:
        bitCounter+=1
        if bitCounter <= (fileBits-extraBits):
            __createPicture__(j)
        else:
            remainingBits.append(j)

for i in range(0, (1080*720)-extraBits):
    remainingBits.append('1')

for j in remainingBits:
    __createPicture__(j)

image_folder = 'pictures'
video_name = 'video.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 1, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
os.system('rm -rf pictures')
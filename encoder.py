#!/usr/bin/python3
from PIL import Image
import os, subprocess, base64, time
import numpy as np
import magic

# Installing opencv
try:
    import cv2
except ImportError or ModuleNotFoundError:
    print('\033[31m[!] CV2 not installed\033[00m')
    print('[+] Installing CV2')
    cv2 = subprocess.check_output(['pip3', 'install', 'opencv-python'], text=True)
    if "Successfully installed" in cv2:
        print('[+] Successfully installed CV2')
        time.sleep(2)
        import cv2
    else:
        print('\033[31m[!] error\033[00m')
        quit()

pixelSet = []
pixel = []
count1080 = 0
count720 = 0
picnumber = 0
bitCounter = 0
pixelX = 1080
pixelY = 720

def __createPicture__(j):
    # catch the set here
    global count1080,count720,pixel,pixelSet,picnumber
    count1080+=1
    if j == '0':
        pixel.append((225, 225, 225))
    elif j == '1':
        pixel.append((0, 0, 0))
    if count1080 == pixelX:
        pixelSet.append(pixel)
        pixel=[]
        count720+=1
        count1080=0
    if count720 == pixelY:
        picnumber+=1
        array = np.array(pixelSet, dtype=np.uint8)
        new_image = Image.fromarray(array)
        new_image.save(f'pictures/new{picnumber}.png')
        pixelSet = []
        count720 = 0

# Searching for file
fileName = input('\033[32m[-] Enter file name: ')
whoAmI = '/home/'
whoAmI+= subprocess.check_output(['whoami'], text=True)
find_file = subprocess.check_output(['find', whoAmI.strip(), '-type', 'f', '-name', fileName], text=True)
fileList = find_file.strip().split('\n')
if len(find_file) == 0:
    print('\033[31m[!] File not found\033[00m')
    quit()
else:
    if len(fileList) > 1:
        num = 0
        for file in fileList:
            num+=1
            print(f'[{num}] : {file}')
        selectedFile = int(input('\n[-] Select File Index Number : '))
        fileName = fileList[selectedFile-1]
    else:
        fileName = fileList[0]

fileType = magic.from_file(fileName).split()[0]

targetFile = open(fileName.strip(), 'rb')
targetFile = targetFile.read()

print('[+] Encoding file')
b64File = base64.b64encode(targetFile)
fileBits = len((b64File)*7)
count = int(fileBits/(pixelX*pixelY))
extraBits = fileBits - count * (pixelX*pixelY)

print('[+] Creating Frames')
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

for i in range(0, (pixelX*pixelY)-extraBits):
    remainingBits.append('1')

for j in remainingBits:
    __createPicture__(j)

image_folder = 'pictures'
video_name = input('[-] Enter desired video name: ')
video_name = f'{video_name}-{fileType.lower()}.avi'
print('[+] Do not remove the file type from the file name')
images = os.listdir(image_folder)
images.reverse()
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
video = cv2.VideoWriter(video_name, 0, 1, (width,height))

print('[+] Compiling Video')
for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
print('[+] CleaningUp!\033[00m')
os.system('rm -rf pictures')
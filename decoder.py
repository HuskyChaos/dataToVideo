#!/usr/bin/python3
from PIL import Image
import os, time, subprocess, base64

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

# Searching for file
fileName = input('\033[32m[-] Enter file name: ')
if fileName[-3:] != 'avi':
    print('\033[31m[!] Invalid file extenssion!\033[00m')
    quit()
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

vid = cv2.VideoCapture(f"{fileName.strip()}")
print('[+] Extracting Frames')
os.system('mkdir outPictures')
currentframe = 1
while(True):
    ret,frame = vid.read()
    if ret:
        name = './outPictures/frame' + str(currentframe) + '.png'
        cv2.imwrite(name, frame)
        currentframe += 1
    else:
        break
vid.release()
cv2.destroyAllWindows()
b64Data = ''
imageList = os.listdir('./outPictures/')
bits = ''
print('[+] Decoding file')
for image in imageList:
    im = Image.open(f'outPictures/{image}')
    imageSizeW, imageSizeH = im.size
    pixel_list = list(im.getdata())
    for i in range(0, imageSizeH):
        for j in range(0, imageSizeW):
            pixVal = im.getpixel((j, i))
            if pixVal[0] == 0 and pixVal[1] == 0 and pixVal[2] == 0:
                if len(bits) == 7:
                    b64Data+=chr(int(bits, 2))
                    bits=''
                    bits+='1'
                else:
                    bits+='1'
            else:
                if len(bits) == 7:
                    b64Data+=chr(int(bits, 2))
                    bits=''
                    bits+='0'
                else:
                    bits+='0'
print('[+] Creating file')
createFile = open(f'decodedFile.{fileName.split("-")[-1].split(".")[-2]}', 'wb')
createFile.write(base64.b64decode(b64Data))
print('[+] CleaningUp!\033[00m')
os.system(f'rm -rf {fileName}')
os.system('rm -rf outPictures')
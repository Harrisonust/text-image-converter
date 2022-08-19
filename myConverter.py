import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont



def cv2ImgAddText(img, text, left, top, textColor=(0, 0, 0), textSize=15):
    if (isinstance(img, numpy.ndarray)):  # 判斷是否OpenCV圖片類型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(
        "font/simsun.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontText)
    return cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)


def wordConvert2mat(img):
    img = cv2ImgAddText(img, targetWord, 0, 0)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, img = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)
    img = cv2.resize(img, RSL)

    return img


while(1):
    RSL = (15, 15)
    targetWords = input("轉換字：")

    for i in range(len(targetWords)):
        img = numpy.zeros((RSL[0], RSL[1], 1), numpy.uint8)
        img.fill(255)
        targetWord = targetWords[i]

        img = wordConvert2mat(img)

        ary = []
        for i in range(RSL[0]):
            for j in range(RSL[1]):
                if img[i][j] == 255:
                    print(chr(12288), end='')
                else:
                    print(targetWord, end='')
            print()
    

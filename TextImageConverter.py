import json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def add_text_to_image(img, text, left, top, text_color=(0, 0, 0), text_size=15):
    if isinstance(img, np.ndarray):  
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    if text in ascii_letters:
        font_text = ImageFont.truetype("font/arial.ttf", text_size)
    else:
        font_text = ImageFont.truetype("font/simsun.ttc", text_size, encoding="utf-8")
    draw.text((left, top), text, text_color, font=font_text)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def convert_word_to_matrix(target_word, width):
    img = np.zeros((width, width, 1), np.uint8)
    img.fill(255)
    img = add_text_to_image(img, target_word, 0, 0, text_size=width)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, img = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    img = cv2.resize(img, (width, width))
    return img

while True:
    width = 15
    target_words = input("Texts to be converted: ")
    
    result = np.empty((len(target_words), width, width), int)

    for index, target_word in enumerate(target_words):
        img = convert_word_to_matrix(target_word, width)
        
        for i in range(width):
            for j in range(width):
                if img[i][j] == 255:
                    print(chr(12288), end='')
                    result[index][i][j] = 0
                else:
                    print(target_word, end='') 
                    result[index][i][j] = 1
            print()

    result_horizontal = np.empty((width, 0), int)
    for word in result:
        result_horizontal = np.hstack((result_horizontal, word))
    
    for i in range(width):
        for j in range(width * len(target_words)):
            if result_horizontal[i][j] == 0:
                print(chr(12288), end='')
            else:
                print(target_words[j // width], end='')
        print()